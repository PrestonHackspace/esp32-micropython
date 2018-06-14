import json
import os

def save(key, value):
    filename = key + '.json'
    f = open(filename, 'w')
    json_str = json.dumps(value)
    f.write(json_str)
    f.close()

def load(key, default = None):
    filename = key + '.json'

    if not filename in os.listdir():
        if default == None:
            raise ValueError()
        return default

    f = open(filename)
    json_str = f.read()
    value = json.loads(json_str)
    f.close()
    return value
