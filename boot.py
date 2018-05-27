from time import sleep

from machine import Pin, I2C
i2c = I2C(scl=Pin(4), sda=Pin(5))

from ssd1306 import SSD1306_I2C
oled = SSD1306_I2C(128, 64, i2c)

oled.fill(0)
oled.text('Starting...', 0, 0)
oled.show()

import network

sta_if = network.WLAN(network.STA_IF)

ap_if = network.WLAN(network.AP_IF)

if not sta_if.isconnected():
    oled.fill(0)
    oled.text('Connecting...', 0, 0)
    oled.show()

    sta_if.active(True)
    sta_if.connect('PPL-IOT-3', 'preston3')

    ap_if.active(True)

    while not sta_if.isconnected():
        oled.fill(0)
        oled.text('Wait...', 0, 0)
        oled.show()

        sleep(1)

        oled.fill(0)
        oled.text('Retry...', 0, 0)
        oled.show()
        pass

oled.fill(0)
oled.text('Connected!', 0, 0)
oled.show()

sleep(1)

oled.fill(0)
oled.text(sta_if.ifconfig()[0], 0, 0)
oled.show()

import gc
gc.collect()

import webrepl
webrepl.start(password='shrimping')


def start_server():
    try:
        import usocket as socket
    except:
        import socket

    import os

    replpath = "webrepl-inlined.html.gz"

    s = socket.socket()
    ai = socket.getaddrinfo("0.0.0.0", 80)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.setblocking(False)
    s.listen(5)

    def accept_handler(sock):
        try:
            res = sock.accept()
        except OSError as e:
            # Non-blocking socket so ignore
            return

        try:
            # print("Handling")
            client_s = res[0]
            string_request = client_s.recv(2048).decode('utf-8')
            # print("Request:" + string_request)

            request_line = string_request.split("\r\n")[0]    # only consider first line
            request_line = request_line.split()     # separate by whitespace
            (request_method, path, request_version) = request_line
            
            header = ''

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

            if src_size != -1 and request_method in ['GET', 'HEAD']:
                header += 'HTTP/1.1 200 OK\r\n'
                if ext == 'jpg':
                    header += 'Content-Type: image/jpeg\r\n'
                else:
                    header += 'Content-Type: text/html; charset=UTF-8\r\n'
                header += 'Content-Encoding: gzip\r\n'
                header += 'Content-Length: ' + str(src_size) + '\r\n'
                header += '\r\n'

                client_s.send(header)

                if request_method == 'GET':
                    with open(src_path, 'r') as f:
                        chunkCount = 0
                        while True:
                            # TODO CH use buffer and readinto
                            chunk = f.read(1024)
                            if chunk != '':
                                client_s.write(chunk)
                                chunkCount = chunkCount + 1
                            else:
                                break
            else:
                header += 'HTTP/1.1 404 Not Found\r\n'
                header += 'Content-Length: 9\r\n'
                header += '\r\n'

                client_s.send(bytes(header, 'ascii'))

                client_s.write(bytes('Not found', 'ascii'))
        except Exception as e:
            print("Exception", e)
        finally:
            client_s.close()

    s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)

gc.collect()


# oled.fill(0)
oled.text('Online', 0, 20)
oled.show()

start_server()
