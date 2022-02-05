

class NetworkManager:
    def __init__(self, level):
        self.queue = []
        self.registry = {}
        self.level = level

    @property
    def all_networks(self):
        nets = []
        for net in self.registry:
            nets += self.registry[net]
        return nets

    def network_update(self, update_network):
        nets = self.registry[update_network.network_type]
        for i in range(len(nets)):
            if nets[i].touches(update_network):
                update_network.merge(nets.pop(i))
                self.network_update(update_network)
                return update_network
        self.registry[update_network.network_type].append(update_network)
        return update_network

    def request(self, block, network_type):

        update_network = network_type(block, self.level)

        if update_network.network_type not in self.registry:
            self.registry[update_network.network_type] = []

        return self.network_update(update_network)

    def update(self):
        for network in self.all_networks:
            network.update()

    def initialize(self):
        for network in self.all_networks:
            network.initialize()
