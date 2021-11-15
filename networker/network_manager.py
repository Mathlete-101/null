from networker.network.enrgy_network import EnergyNetwork


class NetworkManager:
    def __init__(self):
        self.queue = []
        self.registry = {}

    @property
    def all_networks(self):
        nets = []
        for net in self.registry:
           nets.append(net)
        return net

    def request(self, block, network_type):
        if not self.registry.get(network_type):
            self.registry[network_type] = []

        update_network = None
        if network_type == "energy":
            update_network = EnergyNetwork(block)

        if update_network:
            while True:
                for network in self.registry[network_type]:
                    if network.touches(update_network):
                        pass

                break



    def update(self):
        for network in self.all_networks:
            network.update()

    def initialize(self):
        for network in self.all_networks:
            network.initialize()
