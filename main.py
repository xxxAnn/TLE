import discord
from discord.ext.commands import Bot
import bin.settings as settings
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound
from bin.handler import Handle
import bin.secret as token

initial_extensions = ['cogs.management']

BOT_PREFIX = ("TLE_")
client = Bot(command_prefix=BOT_PREFIX, case_insensitive=True)
client.case_insensitive = True

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Bringing communities together", type=1))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    LIST_CHANNELS = Handle.get_list_channels()
    if message.channel.id in LIST_CHANNELS and message.author.id != client.user.id:
        await Handle.process_message(message, client)
    await client.process_commands(message)


@client.event
async def on_message_delete(message):
    LIST_CHANNELS = Handle.get_list_channels()
    if message.channel.id in LIST_CHANNELS and message.author.id == client.user.id:
        await Handle.process_deletion(message, client)
    client.process_command(message)


client.run(token.TOKEN)
