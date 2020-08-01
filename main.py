import secret as tokens
from resource.wsclient import Telephone
import discord
from resource.globals import get_channels
import asyncio


if __name__ == '__main__':
        ws = Telephone('ws://159.203.181.144:6789/')
        try:
            ws.load_addons(token=tokens.SOCKET_TOKEN)
            ws.connect()
            ws.run_forever()
        except KeyboardInterrupt:
            ws.clear_bindings()
            ws.close()
# cd Documents\TLE-SERVER\Examples\02ComplexExample
