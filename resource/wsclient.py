from ws4py.client.threadedclient import WebSocketClient
import threading
import asyncio
import discord
import inspect
import json
import _thread as thread
from discord.ext.commands import Bot
import secret as tokens
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound
from resource.globals import get_channels





class Telephone(WebSocketClient):
    def create_embed(self, **kwargs): # -- username | text | avatar_url | attachment
        embed = discord.Embed(title='{}'.format(kwargs['guild']),color=0x70f76e)
        if kwargs['text'] != "":
            embed.add_field(name="_ _", value='**{1}**: {0}'.format(kwargs['text'], kwargs['username']))
        else:
            embed.set_footer(text="Sent by: {}".format(kwargs['username']))
        if kwargs['attachment'] != "":
            embed.set_image(url=kwargs['attachment'])
        return embed

    def opened(self):
        print('>> Connection started <<')

    def closed(self, code, reason=None):
        self.clear_bindings()
        print('>> Connection closed <<')

    def received_message(self, message):
        recv_str = message.data.decode("utf8")
        parsed = json.loads(recv_str)
        if 'type' in parsed:
            if parsed['type'] == 'message':
                self.run_coro(self.handle_global_message, parsed)
            if parsed['type'] == 'delete':
                self.run_coro(self.handle_global_deletion, parsed)

    def load_addons(self, **kwargs):
        token = kwargs.pop('token', True)
        self.token = token

    def run_coro(self, method, *args):
        process = threading.Thread(target=self.start_coro, args=(method, *args))
        process.start()

    def start_coro(self, method_coro, *args):
        coro = asyncio.run_coroutine_threadsafe(method_coro(*args), self.bot.loop)
        coro.result()

    def telephone_send(self, **kwargs):
        text = kwargs.pop('text', True)
        attachment = kwargs.pop('attachment', True)
        author = kwargs.pop('author')
        guild = kwargs.pop('guild')
        if kwargs:
            raise TypeError("unexpected keyword argument(s) %s" % list(kwargs.keys()))
        dict = {
        'type': 'message',
        'text': text,
        'attachment': attachment,
        'author': author,
        'guild': guild,
        "TOKEN": self.token
        }
        self.send(json.dumps(dict))

    async def handle_global_message(self, message):
        embed = self.create_embed(
        username=message['author']['username'],
        text=message['text'],
        avatar_url = message['author']['avatar_url'],
        attachment=message['attachment'],
        guild=message['guild']
        )
        unique_id = int(message['unique_id'])
        tuple_list = []
        for channel_id in get_channels():
            try:
                channel = self.bot.get_channel(int(channel_id))
                msg = await channel.send(embed=embed)
                tpl = (channel.id, msg.id)
                tuple_list.append(tpl)
            except Exception as e:
                continue
        self.append_binding(unique_id=unique_id, content=tuple_list)

    def append_binding(self, **kwargs):
        unique_id = kwargs.get('unique_id')
        content = kwargs.get('content')
        with open('bin/bindings.json', 'r') as f:
            cache = json.loads(f.read())
            f.close()
        cache[str(unique_id)] = content
        with open('bin/bindings.json', 'w') as f:
            f.write(json.dumps(cache))

    def clear_bindings(self):
        with open('bin/bindings.json', 'r') as f:
            cache = json.loads(f.read())
            f.close()
        cache = {}
        with open('bin/bindings.json', 'w') as f:
            f.write(json.dumps(cache))

    async def handle_discord_message(self, message):
        if len(message.attachments) > 0:
            att = message.attachments[0].proxy_url
        else:
            att = ""
        author_dict = {"username": message.author.name, "avatar_url": ""}
        # --
        self.telephone_send(text=message.content, attachment=att, author=author_dict, guild=message.guild.name)
        await message.delete()

    async def handle_discord_deletion(self, message):
        with open('bin/bindings.json', 'r') as f:
            cache = json.loads(f.read())
            f.close()
        for key, values in cache.items():
            for tuple in values:
                if message.id in tuple:
                    id = int(key)
                    break
        if id:
            dict = {
            "type": "delete",
            "unique_id": id,
            "TOKEN": tokens.SOCKET_TOKEN
            }
            smsg = json.dumps(dict)
            x = self.send(smsg)
        else:
            raise KeyError

    async def handle_global_deletion(self, message):
        with open('bin/bindings.json', 'r') as f:
            cache = json.loads(f.read())
            f.close()
        tuple_list = None
        if str(message.get('unique_id')) in cache.keys():
            tuple_list = cache[str(message.get('unique_id'))]
        if tuple_list:
            for tuple in tuple_list:
                try:
                    channel_id = tuple[0]
                    message_id = tuple[1]
                    msg = await self.bot.get_channel(int(channel_id)).fetch_message(int(message_id))
                    await msg.delete()
                except Exception as e:
                    print(e)
                    continue
        else:
            raise KeyError
