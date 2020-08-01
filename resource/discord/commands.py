import discord
from discord.ext import commands
import random
import time
import inspect
import json
managers = [169507259171340289, 423829836537135108, 331431342438875137, 671500917295546408, 282965966386757632, 289798359915560961, 497582475091116042]


class cmds(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def POP_CHANNEL(self, ctx, channel_id: int):
        if ctx.author.id in managers:
            with open('bin/channels.json', 'r') as f:
                cache = json.loads(f.read())
                f.close()
            # --
            try:
                cache.remove(int(channel_id))
            except ValueError:
                return
            with open('bin/channels.json', 'w') as f:
                f.write(json.dumps(cache, sort_keys=True, indent=4, separators=(',', ': ')))
                f.close()
            await ctx.send("Operation successful")
        else:
            await ctx.send("This bot is currently private")


    @commands.command()
    async def ADD_CHANNEL(self, ctx, channel_id: int):
        if ctx.author.id in managers:
            with open('bin/channels.json', 'r') as f:
                cache = json.loads(f.read())
                f.close()
            # --
            try:
                cache.append(int(channel_id))
            except ValueError:
                return
            with open('bin/channels.json', 'w') as f:
                f.write(json.dumps(cache, sort_keys=True, indent=4, separators=(',', ': ')))
                f.close()
            await ctx.send("Operation successful")
        else:
            await ctx.send("This bot is currently private")

def setup(bot):
    bot.add_cog(cmds(bot))
