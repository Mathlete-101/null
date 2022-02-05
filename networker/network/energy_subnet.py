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
        print(self.connections)
        for block in self.connections:
            if block.supplying:
                self.on()
                self.supplying = True
                self.power_update_connections()
                return
        self.off()
        self.supplying = False
        self.power_update_connections()
