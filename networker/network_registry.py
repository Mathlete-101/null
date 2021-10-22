network_registry = {}


def get(network):
    return network_registry[network]


def add(network, name):
    network_registry[name] = network
