import discord
import json
from discord.ext import commands

class Management(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def POP_CHANNEL(self, ctx, channel_id: int):
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

    @commands.command()
    async def ADD_CHANNEL(self, ctx, channel_id: int):
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

def setup(bot):
    bot.add_cog(Management(bot))
