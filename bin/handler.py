import bin.settings as settings
import discord
import discord.ext
from discord.ext.commands import Bot
import json
import asyncio

class Handle:

    @staticmethod
    async def create_embed(message):
        embed = discord.Embed(title='Guild: {}'.format(message.guild.name),color=0x70f76e)
        if message.content != "":
            embed.add_field(name="Message:", value=message.content)
        if len(message.attachments)>0:
            embed.set_image(url=message.attachments[0].url)
        embed.set_footer(text="Sent by: {}".format(message.author.name), icon_url=message.author.avatar_url)
        return embed


    @staticmethod
    def get_list_channels(**kwargs):
        with open('bin/channels.json', 'r') as f:
            return json.loads(f.read())

    @staticmethod
    async def process_deletion(message, client):
        tuple = await Handle.get_tuple(message)
        if tuple != None:
            for elem in tuple:
                message_id = int(elem[0])
                channel_id = int(elem[1])
                try:
                    message = await client.get_channel(channel_id).fetch_message(message_id)
                    await message.delete()
                except:
                    continue

    @staticmethod
    async def get_tuple(message):
        with open('bin/cache/deleter.json', 'r') as f:
            cache = json.loads(f.read())
            f.close()
        # --
        if isinstance(cache, list):
            for tuple in cache:
                for pair in tuple:
                    if str(message.id) in pair:
                        return tuple
        else:
            raise TypeError
        return None

    @staticmethod
    async def add_message_to_cache(list_message):
        with open('bin/cache/deleter.json', 'r') as f:
            current_cache = json.loads(f.read())
            f.close()
        # --
        if isinstance(current_cache, list):
            if len(current_cache) > settings.LOG_LENGTH:
                del current_cache[:1]
            current_cache.append(list_message)
        else:
            raise TypeError
        with open('bin/cache/deleter.json', 'w') as f:
            f.write(json.dumps(current_cache, sort_keys=True, indent=4, separators=(',', ': ')))
            f.close()

    @staticmethod
    async def process_message(message, bot):
        content = message.content
        embed = await Handle.create_embed(message)
        try:
            asyncio.wait(0.2)
            await message.delete()
        except discord.ext.commands.errors.MissingPermissions:
            await message.channel.send("Missing permission")
            return
        list_message = []
        for channel_id in Handle.get_list_channels():
            channel = bot.get_channel(channel_id)
            if channel == None: continue
            message = await channel.send(embed=embed)
            list_message.append((str(message.id) ,str(message.channel.id)))
        await Handle.add_message_to_cache(list_message)
