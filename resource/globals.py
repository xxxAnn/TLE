import json


def get_channels():
    with open('bin/channels.json', 'r') as f:
        parsed = json.loads(f.read())
        f.close()
    return parsed
