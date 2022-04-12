from networker.network.network import Network


class EnergySubnet(Network):
    def __init__(self, obj, level):
        super().__init__(obj, level)
        self.network_type = "energy_subnet"
        self.is_on = False
        self.connections = []
        self.supplying = False

    def on(self):
        self.is_on = True
        for obj in self.objects:
            obj.on()

    def off(self):
        self.is_on = False
        for obj in self.objects:
            obj.off()

    def merge(self, network):
        super().merge(network)
        self.connections += network.connections
        for connection in network.connections:
            connection.connected = self

    def power_update_connections(self):
        for obj in self.connections:
            obj.power_update()

    def power_update(self):
        for block in self.connections:
            if block.supplying:
                self.on()
                self.supplying = True
                self.power_update_connections()
                return
        self.off()
        self.supplying = False
        self.power_update_connections()

    def get_minimum_removal_distance_connection(self):
        """Gets the item in connections with the smallest value when get_removal_distance is called"""
        item = min(filter(lambda x: x.supplying, self.connections), key=lambda x: x.get_removal_distance())
        return item

    def remove_energy(self):
        self.get_minimum_removal_distance_connection().remove_energy()

    def get_removal_distance(self):
        return self.get_minimum_removal_distance_connection().get_removal_distance() + 1


