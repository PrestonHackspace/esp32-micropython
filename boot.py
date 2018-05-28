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


# def parse_post_data(post_data) -> dict:
#     pairs = post_data.split('&')

#     params = {}

#     for [key, value] in pairs:
#         params[key] = value

#     return params


def start_server():
    try:
        import usocket as socket
    except:
        import socket

    import os
    import json

    s = socket.socket()
    ai = socket.getaddrinfo("0.0.0.0", 80)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.setblocking(False)
    s.listen(5)

    def accept_handler(sock):
        try:
            (client_s, _) = sock.accept()
        except OSError as e:
            # Non-blocking socket so ignore
            return

        printLine('ACCEPT', 3)

        try:
            client_s.settimeout(1)

            string_request = client_s.recv(2048).decode('utf-8')

            printLine(string_request, 4)

            request_lines = string_request.split("\r\n")

            # only consider first line
            request_line = request_lines[0]
            # separate by whitespace
            request_line = request_line.split()

            if len(request_line) < 3:
                return

            (request_method, path, _) = request_line

            header = ''

            if request_method == 'POST':
                if path == '/networks.json':
                    network_list = get_network_list()

                    data = bytes(json.dumps(network_list), 'utf-8')

                    header += 'HTTP/1.1 200 OK\r\n'
                    header += 'Content-Type: application/json\r\n'
                    header += 'Content-Length: ' + str(len(data)) + '\r\n'
                    header += '\r\n'

                    client_s.send(bytes(header, 'utf-8'))

                    client_s.write(data)

                if path == '/connect.json':
                    post_data = request_lines[2]

                    # params = parse_post_data(post_data)

                    params = json.loads(post_data)

                    ssid = params['ssid']
                    password = params['pass']

                    ip_address = do_connect(ssid, password)

                    data = bytes(json.dumps(ip_address), 'utf-8')

                    header += 'HTTP/1.1 200 OK\r\n'
                    header += 'Content-Type: application/json\r\n'
                    header += 'Content-Length: ' + str(len(data)) + '\r\n'
                    header += '\r\n'

                    client_s.send(bytes(header, 'utf-8'))

                    client_s.write(data)

            elif request_method in ['GET', 'HEAD']:
                if path == '/':
                    path = '/index.html'

                parts = path.split('.')
                ext = parts[len(parts) - 1]

                src_path = 'web' + path + '.gz'
                src_size = -1

                try:
                    src_size = os.stat(src_path)[6]
                except Exception as e:
                    pass

                if src_size != -1:
                    header += 'HTTP/1.1 200 OK\r\n'
                    header += 'Connection: close\r\n'
                    if ext == 'jpg':
                        header += 'Content-Type: image/jpeg\r\n'
                    else:
                        header += 'Content-Type: text/html; charset=UTF-8\r\n'
                    header += 'Content-Encoding: gzip\r\n'
                    header += 'Content-Length: ' + str(src_size) + '\r\n'
                    header += '\r\n'

                    client_s.send(bytes(header, 'utf-8'))

                    if request_method == 'GET':
                        with open(src_path, 'r') as f:
                            while True:
                                # TODO CH use buffer and readinto
                                chunk = f.read(1024)
                                if chunk != '':
                                    client_s.write(chunk)
                                else:
                                    break
                else:
                    header += 'HTTP/1.1 404 Not Found\r\n'
                    header += 'Connection: close\r\n'
                    header += 'Content-Length: 9\r\n'
                    header += '\r\n'

                    client_s.send(bytes(header, 'utf-8'))

                    client_s.write(bytes('Not found', 'utf-8'))
        except Exception as e:
            print("Exception", e)
        finally:
            client_s.close()
            printLine('CLOSED', 3)

    s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)


gc.collect()


printLine('Online', 0)

start_server()

counter = store.load('counter', 0)

printLine(str(counter), 2)

counter = counter + 1

store.save('counter', counter)
