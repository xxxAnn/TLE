import secret as tokens
from resource.wsclient import Telephone
import discord
from resource.globals import get_channels
import asyncio
import _thread as thread
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound


BOT_PREFIX = ("TLE2_")
client = Bot(command_prefix=BOT_PREFIX, case_insensitive=True)
client.case_insensitive = True


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(activity=discord.Game(name="Bringing communities together", type=1))
    client.load_extension('resource.discord.commands')
    def call_phone():
        ws = Telephone('ws://159.203.181.144:6789/')
        ws.bot = client
        client.telephone = ws
        try:
            ws.load_addons(token=tokens.SOCKET_TOKEN)
            ws.connect()
            ws.run_forever()
        except KeyboardInterrupt:
            ws.clear_bindings()
            ws.close()
    thread.start_new_thread(call_phone, ())



@client.event
async def on_message_delete(message):
    if message.channel.id in get_channels() and message.author.id == client.user.id:
        await client.telephone.handle_discord_deletion(message)


@client.event
async def on_message(message):
    if message.channel.id in get_channels() and message.author.id != client.user.id:
        await client.telephone.handle_discord_message(message)
    await client.process_commands(message)

if __name__ == '__main__':
    client.run(tokens.DISCORD_TOKEN)

# cd Documents\TLE-SERVER\Examples\02ComplexExample
