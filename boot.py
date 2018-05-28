from time import sleep

from screen import printLine

printLine('Starting...', 0)

import network
import store

wifi_config = store.load('wifi')

sta_if = network.WLAN(network.STA_IF)

ap_if = network.WLAN(network.AP_IF)

if not sta_if.isconnected():
    printLine('Connecting...', 0)

    sta_if.active(True)
    sta_if.connect(wifi_config['ssid'], wifi_config['pass'])

    ap_if.active(True)

    while not sta_if.isconnected():
        printLine('Wait...', 0)

        sleep(1)

        printLine('Retry...', 0)
        pass

printLine('Connected!', 0)

sleep(1)

printLine(sta_if.ifconfig()[0], 1)

import gc
gc.collect()

import webrepl
webrepl.start(password='')


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


def do_connect(ssid, password) -> str:
    sta_if.active(True)

    print('Trying to connect to %s...' % ssid)

    sta_if.connect(ssid, password)

    for _ in range(100):
        connected = sta_if.isconnected()

        if connected:
            break

        sleep(0.1)

        print('.', end='')

    ip_address = sta_if.ifconfig()[0]

    if connected:
        print('\nConnected. Network config: ', ip_address)
        return ip_address
    else:
        print('\nFailed. Not Connected to: ' + ssid)
        return None


gc.collect()


printLine('Online', 0)

import http


def handler(method, path, post_data):
    if path == '/':
        return {'file': 'index.html'}

    if path == '/networks.json':
        network_list = get_network_list()

        return {'json': network_list}


http.start_server(handler)

# start_server()

counter = store.load('counter', 0)

printLine(str(counter), 2)

counter = counter + 1

store.save('counter', counter)
