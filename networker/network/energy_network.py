from typing import List

import tools.duple
import tools.lists
from animation.animation import Animation
from effect.effect import Effect
from networker.network.energy_subnet import EnergySubnet
from networker.network.network import Network
from graphics import graphics
from networker.network_manager import NetworkManager
from tools.ticker import Ticker


class EnergyNetwork(Network):

    def __init__(self, obj, level):
        super().__init__(obj, level)
        self.network_type = "energy"
        self.wirenet_manager = NetworkManager(level)
        self.update_tickers = []

    # def laser(self, magnitude, block):
        # block.on()
        # self.receiver_tickers.append((Ticker(60), block))

        # for net in self.subnet_manager.registry["energy_subnet"]:
        #     if net.touches_block(block):
        #         net.on()
        # pass

    def update_for(self, block, time):
        ticker = Ticker(time)
        self.update_tickers.append((ticker, block))
        return ticker

    def initialize(self):
        for obj in self.objects:
            self.the_complicated_part(obj)
        for obj in self.objects:
            obj.initialize()

    def update(self):
        for obj in set([x[1] for x in self.update_tickers]):
            obj.update()
        done, self.update_tickers = tools.lists.extract(self.update_tickers, lambda t: t[0].tick())

    def the_complicated_part(self, block):
        possibly_relevant_stuff = []
        relevant_stuff = []
        for obj in self.objects:
            if tools.duple.adjacent(obj.location, block.location):
                possibly_relevant_stuff.append(obj)

        # try to connect with stuff
        # for wires
        if "wire" in block.tags:
            net: EnergySubnet = self.wirenet_manager.request(block, EnergySubnet)
            for item in possibly_relevant_stuff:
                if "wire" not in item.tags:
                    success, connection = item.attempt_connection(net, block.location)
                    if success:
                        net.connections.append(connection)
                        # perform auto orientation on the item (if needed)
                        if "energy_receptive" in item.tags or "force_field" in item.tags:
                            graphic = None
                            if "timed" in item.tags:
                                graphic = graphics.get("energy_receiver_time")
                            elif "toggle" in item.tags:
                                graphic = graphics.get("energy_receiver_toggle")
                            elif "force_field" in item.tags:
                                graphic = graphics.get("energy_force_field")

                            if block.location[0] > item.location[0]:
                                item.graphic = graphic.get_rotation(-90)
                                orientation = (-1, 0)
                            elif block.location[0] < item.location[0]:
                                item.graphic = graphic.get_rotation(90)
                                orientation = (1, 0)
                            elif block.location[1] > item.location[1]:
                                item.graphic = graphic.get_rotation(180)
                                orientation = (0, -1)
                            else:
                                item.graphic = graphic
                                orientation = (0, 1)

                            if "force_field" in item.tags:
                                item.orientation = orientation

                        relevant_stuff.append(item)
                else:
                    relevant_stuff.append(item)

        # for non wires
        # for now, I'm just going to not do this.
        if "wire" not in block.tags:
            for item in possibly_relevant_stuff:
                if "wire" not in item.tags and block.can_connect(item.location):
                    success, connection = item.attempt_connection(block, block.location)
                    if success:
                        relevant_stuff.append(item)

        # automatic orientation
        if "wire" in block.tags:
            # figure out if it needs to be a dark wire
            if "dark" in block.tags:
                dark = "_dark"
            else:
                dark = ""
            if len(relevant_stuff) == 1:
                if relevant_stuff[0].location[1] == block.location[1]:
                    block.graphic = graphics.get("energy_wire_through" + dark).get_rotation(90)
                    return
            elif len(relevant_stuff) == 2:

                # straights
                if relevant_stuff[0].location[1] == block.location[1] == relevant_stuff[1].location[1]:
                    block.graphic = graphics.get("energy_wire_through" + dark).get_rotation(90)
                    return
                elif relevant_stuff[0].location[0] == block.location[0] == relevant_stuff[1].location[0]:
                    block.graphic = graphics.get("energy_wire_through" + dark)
                    return

                # corners
                if relevant_stuff[1].location[1] != block.location[1]:
                    # switch them if the one on the top is second
                    relevant_stuff.append(relevant_stuff.pop(0))
                vert = relevant_stuff[0].location[1] > block.location[1]
                hor = relevant_stuff[1].location[0] > block.location[0]
                if vert:
                    if hor:
                        block.graphic = graphics.get("energy_wire_turn" + dark)
                    else:
                        block.graphic = graphics.get("energy_wire_turn" + dark).get_rotation(-90)
                else:
                    if hor:
                        block.graphic = graphics.get("energy_wire_turn" + dark).get_rotation(90)
                    else:
                        block.graphic = graphics.get("energy_wire_turn" + dark).get_rotation(180)
            elif len(relevant_stuff) == 3:
                # t junctions
                # I don't know which is x and which is y so they are just 2 and 3
                rel1 = [block.location[0] - x.location[0] for x in relevant_stuff]
                rel2 = [block.location[1] - x.location[1] for x in relevant_stuff]

                t_junction = graphics.get("energy_wire_t_junction" + dark)

                if 1 not in rel1:
                    block.graphic = t_junction.get_rotation(90)
                elif -1 not in rel1:
                    block.graphic = t_junction.get_rotation(-90)
                elif 1 not in rel2:
                    block.graphic = t_junction
                else:
                    block.graphic = t_junction.get_rotation(180)
            elif len(relevant_stuff) == 4:
                # cross junction
                # this is easy
                block.graphic = graphics.get("energy_wire_cross_junction" + dark)

        elif "energy_receptive" in block.tags:
            if len(relevant_stuff) != 0:
                graphic = None
                if "timed" in block.tags:
                    graphic = graphics.get("energy_receiver_time")
                elif "toggle" in block.tags:
                    graphic = graphics.get("energy_receiver_toggle")

                if relevant_stuff[0].location[0] > block.location[0]:
                    block.graphic = graphic.get_rotation(-90)
                elif relevant_stuff[0].location[0] < block.location[0]:
                    block.graphic = graphic.get_rotation(90)
                elif relevant_stuff[0].location[1] > block.location[1]:
                    block.graphic = graphic.get_rotation(180)
                else:
                    block.graphic = graphic
