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

if not sta_if.isconnected():    
    oled.fill(0)
    oled.text('Connecting...', 0, 0)
    oled.show()

    sta_if.active(True)
    sta_if.connect('PPL-IOT-3', 'preston3')

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
            #print("Handling")
            client_s = res[0]
            string_request = client_s.recv(2048).decode('utf-8')
            #print("Request:" + string_request)
            
            request_line = string_request.split("\r\n")[0]    # only consider first line
            request_line = request_line.split()     # separate by whitespace 
            (request_method, path, request_version) = request_line
            header = ''
            content = ''
            if request_method == "GET" and "favicon" not in path:
                #print("GET "+ path)
                header += 'HTTP/1.1 200 OK\r\n'
                header += 'Content-Type: text/html; charset=UTF-8\r\n'
                header += 'Content-Encoding: gzip\r\n'

                replsize = os.stat(replpath)[6]
                header += 'Content-Length: ' + str(replsize) + '\r\n'
                header += '\r\n'

                client_s.send(header)
                #print("Sent "+ header)
                
                with open(replpath, 'r') as f:
                    chunkCount = 0
                    while True:
                        # TODO CH use buffer and readinto
                        chunk = f.read(1024)
                        if chunk != '':
                            client_s.write(chunk)
                            #print("Sent chunk " + str(chunkCount) + ":" + str(len(chunk)))
                            chunkCount = chunkCount + 1
                        else:
                            #print("Last chunk sent")
                            break		
        except Exception as e:
            print("Exception", e)
        finally:
            client_s.close()

    s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)

gc.collect()

oled.fill(0)
oled.text('Online', 0, 0)
oled.show()

start_server()
