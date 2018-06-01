import wifi
import http


def handler(method, path, post_json):
    if path == '/':
        return {'file': 'index.html'}

    if path == '/status.json':
        status = wifi.get_status()

        return {'json': status}

    if path == '/network_list.json':
        network_list = wifi.get_network_list()

        return {'json': network_list}

    if path == '/network_saved_list.json':
        network_list = wifi.list_saved()

        return {'json': network_list}

    if method == 'POST' and path == '/api':
        method = post_json['method']

        if method == 'connect':
            ssid = post_json['ssid']
            password = post_json['pass']

            ip_address = wifi.connect_and_save(ssid, password)

            if ip_address == None:
                return {'json': {'status': 'failed'}}

            return {'json': {'status': 'connected', 'ip_address': ip_address}}

        if method == 'connect_saved':
            ssid = post_json['ssid']

            ip_address = wifi.connect_to_saved(ssid)

            if ip_address == None:
                return {'json': {'status': 'failed'}}

            return {'json': {'status': 'connected', 'ip_address': ip_address}}


def start_panel():
    http.start_server(handler)
