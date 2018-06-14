import os
import json


def listdir(cwd = '.'):
    filenames = os.listdir(cwd)

    files = []

    for filename in filenames:
        status = os.stat(cwd + '/' + filename)

        files.append({
            'filename': filename,
            'isdir': True if status[0] & 16384 else False
        })

    return files
