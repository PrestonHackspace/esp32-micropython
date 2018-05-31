from screen import printLine
import socket
import os
import json

# def parse_post_data(post_data) -> dict:
#     pairs = post_data.split('&')

#     params = {}

#     for [key, value] in pairs:
#         params[key] = value

#     return params


def start_server(handler):
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

            string_request = client_s.recv(4096).decode('utf-8')

            printLine(string_request, 4)

            request_lines = string_request.split("\r\n")
            request_line = request_lines[0]
            request_line = request_line.split()

            if len(request_line) < 3:
                return

            (request_method, path, _) = request_line

            header = ''
            post_json = {}

            def respond_with_cors():
                header = ''

                header += 'HTTP/1.1 200 OK\r\n'
                header += 'Accept: application/json\r\n'
                header += 'Access-Control-Allow-Origin: *\r\n'
                header += 'Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n'
                header += 'Access-Control-Allow-Headers: content-type\r\n'
                header += 'Content-Length: 0\r\n'
                header += '\r\n'

                client_s.write(bytes(header, 'utf-8'))

            def respond_with_error(code, message):
                header = ''

                header += 'HTTP/1.1 ' + str(code) + ' Invalid Request\r\n'
                header += 'Content-Length: ' + str(len(message)) + '\r\n'
                header += '\r\n'

                client_s.send(bytes(header, 'utf-8'))

                client_s.write(bytes(message, 'utf-8'))

            if request_method == 'OPTIONS':
                return respond_with_cors()

            if request_method == 'POST':
                post_data = request_lines[len(request_lines) - 1]

                try:
                    post_json = json.loads(post_data)
                except:
                    return respond_with_error('400', 'Invalid JSON: ' + post_data)

            response = handler(request_method, path, post_json)

            if not response:
                response = { 'file': path }

            if 'json' in response:
                data = bytes(json.dumps(response['json']), 'utf-8')

                header += 'HTTP/1.1 200 OK\r\n'
                header += 'Access-Control-Allow-Origin: *\r\n'
                header += 'Content-Type: application/json\r\n'
                header += 'Content-Length: ' + str(len(data)) + '\r\n'
                header += '\r\n'

                client_s.send(bytes(header, 'utf-8'))

                client_s.write(data)

            if 'file' in response:
                file = response['file']

                parts = file.split('.')
                ext = parts[len(parts) - 1]

                src_path = 'web/' + file + '.gz'
                src_size = -1

                try:
                    src_size = os.stat(src_path)[6]
                except Exception as e:
                    pass

                if src_size != -1:
                    header += 'HTTP/1.1 200 OK\r\n'
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
                    respond_with_error(404, 'File not found')
            else:
                respond_with_error(404, 'Not found')

        except Exception as e:
            print("Exception", e)
        finally:
            client_s.close()
            printLine('CLOSED', 3)

    s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)
