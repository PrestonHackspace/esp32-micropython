import socket
import os
import json
import _thread


def get_file(file):
    src_size = -1

    try:
        src_path = 'web/' + file + '.gz'
        src_size = os.stat(src_path)[6]

        return [src_path, src_size, 'gzip']
    except Exception:
        pass

    return [None, -1, None]


def get_content_type(ext):
    if ext == 'jpg':
        return 'image/jpeg'
    elif ext == 'png':
        return 'image/png'
    elif ext == 'css':
        return 'text/css'
    elif ext == 'js':
        return 'text/javascript'
    elif ext == 'txt':
        return 'text/plain'
    elif ext == 'mp3':
        return 'audio/mpeg'
    elif ext == 'wav':
        return 'audio/wav'
    elif ext == 'cur' or ext == 'ico':
        return 'image/x-icon'
    else:
        return 'text/html; charset=UTF-8'


def _start_server(handler):
    s = socket.socket()
    ai = socket.getaddrinfo("0.0.0.0", 80)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.setblocking(True)
    s.listen(5)

    while True:
        sock = s

        (client_s, _) = sock.accept()

        try:
            client_s.settimeout(3)

            buf = None
            bufs = None

            while True:
                chunk = client_s.recv(128)

                if buf == None:
                    buf = chunk
                else:
                    buf += chunk

                bufs = buf.decode('utf-8')

                if '\r\n\r\n' in bufs:
                    break

            lines = bufs.split("\r\n")

            first_line_parts = lines[0].split()

            if len(first_line_parts) < 3:
                return

            (request_method, path, _) = first_line_parts

            header = ''
            post_json = {}

            def respond_with_cors():
                header = ''

                header += 'HTTP/1.1 200 OK\r\n'
                header += 'Accept: application/json\r\n'
                header += 'Access-Control-Allow-Origin: *\r\n'
                header += 'Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n'
                header += 'Access-Control-Allow-Headers: content-type, x-json\r\n'
                header += 'Content-Length: 0\r\n'
                header += '\r\n'

                client_s.sendall(bytes(header, 'utf-8'))

            def respond_with_error(code, message):
                header = ''

                header += 'HTTP/1.1 ' + str(code) + ' Invalid Request\r\n'
                header += 'Content-Type: text/plain\r\n'
                header += 'Content-Length: ' + str(len(message)) + '\r\n'
                header += '\r\n'

                # f = open('dump.json', 'w')
                # f.write(json.dumps(lines))
                # f.close()

                client_s.sendall(bytes(header, 'utf-8'))

                client_s.sendall(bytes(message, 'utf-8'))

            if request_method == 'OPTIONS':
                return respond_with_cors()

            if request_method == 'POST':
                json_str = '{}'

                for line in lines:
                    try:
                        if line.index('x-json') == 0:
                            (_, json_str) = line.split(': ')
                    except ValueError as e:
                        pass

                try:
                    post_json = json.loads(json_str)
                except:
                    return respond_with_error('400', 'Invalid JSON: ' + json_str)

            response = handler(request_method, path, post_json)

            if not response:
                response = {'file': path}

            if 'json' in response:
                data = bytes(json.dumps(response['json']), 'utf-8')

                header += 'HTTP/1.1 200 OK\r\n'
                header += 'Access-Control-Allow-Origin: *\r\n'
                header += 'Content-Type: application/json\r\n'
                header += 'Content-Length: ' + str(len(data)) + '\r\n'
                header += '\r\n'

                client_s.sendall(bytes(header, 'utf-8'))

                client_s.sendall(data)

            if 'file' in response:
                file = response['file']

                parts = file.split('.')
                ext = parts[len(parts) - 1]

                [src_path, src_size, src_enc] = get_file(file)

                content_type = get_content_type(ext)

                if src_size != -1:
                    header += 'HTTP/1.1 200 OK\r\n'
                    header += 'Content-Type: ' + content_type + '\r\n'
                    header += 'Content-Encoding: ' + src_enc + '\r\n'
                    header += 'Content-Length: ' + str(src_size) + '\r\n'
                    header += '\r\n'

                    client_s.sendall(bytes(header, 'utf-8'))

                    if request_method == 'GET':
                        with open(src_path, 'r') as f:
                            while True:
                                # TODO CH use buffer and readinto
                                chunk = f.read(1024)
                                if chunk != '':
                                    client_s.sendall(chunk)
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


def start_server(handler):
    _thread.start_new_thread(_start_server, (handler,))
