import store

def get_network_saved_list():
    return store.load('networks', [])


def add_network_saved(network):
    if not 'ssid' in network:
        raise ValueError()

    if not 'pass' in network:
        raise ValueError()

    network_saved_list = store.load('networks', [])

    # Remove a previous entry if it was there...
    network_saved_list = [
        x for x in network_saved_list if x['ssid'] != network['ssid']]

    network_saved_list.append(network)

    store.save('networks', network_saved_list)