from screen import printLine

printLine('Starting...', 0)

from time import sleep

import network
import store
import json
import gc

ap_if = network.WLAN(network.AP_IF)
sta_if = network.WLAN(network.STA_IF)

ap_if.active(True)
sta_if.active(True)

# wifi_config = store.load('wifi', None)

# if wifi_config != None and not sta_if.isconnected():
#     printLine('Connecting...', 0)

#     sta_if.active(True)
#     sta_if.connect(wifi_config['ssid'], wifi_config['pass'])

#     while not sta_if.isconnected():
#         printLine('Wait...', 0)

#         sleep(1)

#         printLine('Retry...', 0)
#         pass

#     printLine('Connected!', 0)

# sleep(1)

# printLine(sta_if.ifconfig()[0], 1)

gc.collect()


def get_status():
    status = {
        'ap': ap_if.ifconfig(),
        'sta': sta_if.ifconfig(),
    }

    return json.dumps(status)


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


def get_network_list():
    networks = sta_if.scan()

    network_list = []

    for ssid, _, channel, rssi, authmode, hidden in sorted(networks, key=lambda x: x[3], reverse=True):
        ssid = ssid.decode('utf-8')

        network_list.append({
            'ssid': ssid,
            'channel': channel,
            'rssi': rssi,
            'authmode': authmode,
            'hidden': hidden
        })

    return network_list


def connect(ssid, password) -> str:
    sta_if.active(True)

    printLine('Connect %s...' % ssid, 0)

    sta_if.connect(ssid, password)

    for attempt in range(10):
        connected = sta_if.isconnected()

        if connected:
            break

        sleep(1)

        printLine('Attempt %i' % attempt, 1)

    if connected:
        ip_address = sta_if.ifconfig()[0]

        printLine('Connected! %s' % ssid, 0)
        printLine('IP %s' % ip_address, 0)

        add_network_saved({'ssid': ssid, 'pass': password})

        return ip_address
    else:
        printLine('Failed!', 0)

        return None


def connect_saved(ssid) -> str:
    network_saved_list = get_network_saved_list()

    matches = [x for x in network_saved_list if x['ssid'] == ssid]

    if len(matches) == 0:
        return None

    network_saved = matches[0]
    password = network_saved['pass']

    sta_if.active(True)

    printLine('Connect %s...' % ssid, 0)

    sta_if.connect(ssid, password)

    for attempt in range(10):
        connected = sta_if.isconnected()

        if connected:
            break

        sleep(1)

        printLine('Attempt %i' % attempt, 1)

    if connected:
        ip_address = sta_if.ifconfig()[0]

        printLine('Connected! %s' % ssid, 0)
        printLine('IP %s' % ip_address, 1)

        return ip_address
    else:
        printLine('Failed!', 0)

        return None


def list_saved() -> list:
    network_list = get_network_list()

    network_saved_list = get_network_saved_list()

    results = []

    for network_saved in network_saved_list:
        matches = [x for x in network_list if x['ssid']
                   == network_saved['ssid']]

        result = {
            'ssid': network_saved['ssid'],
            'saved': True
        }

        if len(matches) > 0:
            network = matches[0]

            result['channel'] = network['channel']
            result['rssi'] = network['rssi']

        results.append(result)

    return results


def auto_connect():
    networks_merged = list_saved()

    if len(networks_merged) > 0:
        strongest_network = networks_merged[0]

        if 'rssi' in strongest_network:
            connect_saved(strongest_network['ssid'])


auto_connect()

gc.collect()

import webrepl
webrepl.start(password='')


printLine('Online', 0)

import http


def handler(method, path, post_json):
    if path == '/':
        return {'file': 'index.html'}

    if path == '/status.json':
        status = get_status()

        return {'json': status}

    if path == '/network_list.json':
        network_list = get_network_list()

        return {'json': network_list}

    if path == '/network_saved_list.json':
        network_list = list_saved()

        return {'json': network_list}

    if method == 'POST' and path == '/api':
        method = post_json['method']

        if method == 'connect':
            ssid = post_json['ssid']
            password = post_json['pass']

            ip_address = connect(ssid, password)

            if ip_address == None:
                return {'json': {'status': 'failed'}}

            return {'json': {'status': 'connected', 'ip_address': ip_address}}

        if method == 'connect_saved':
            ssid = post_json['ssid']

            ip_address = connect_saved(ssid)

            if ip_address == None:
                return {'json': {'status': 'failed'}}

            return {'json': {'status': 'connected', 'ip_address': ip_address}}


http.start_server(handler)

counter = store.load('counter', 0)

printLine(str(counter), 2)

counter = counter + 1

store.save('counter', counter)
