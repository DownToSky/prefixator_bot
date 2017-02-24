import discord
import asyncio
from discord.ext import commands
import utils


def setup(bot):
    bot.add_cog(Prefix(bot))
    print("{} module loaded".format(__file__))

class Prefix:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "setprefix", pass_context = True)
    async def set_prefix(self, ctx, *, inputs:str):
        server_id = ctx.message.server.id
        if self.bot.configs["servers"][server_id]["enforce_prefix"] == False:
            self.bot.configs["servers"][server_id]["enforce_prefix"] = True
        else:
            await self.bot.deprefixate_server(ctx.message.server)
        self.bot.configs["servers"][server_id]["prefix"] = inputs
        await self.bot.prefixate_server(ctx. message.server)

    @commands.command(name = "removeprefix", pass_context = True)
    async def remove_prefix(self, ctx):
        server_id = ctx.message.server.id
        await self.bot.deprefixate_server(ctx.message.server)
        self.bot.configs["servers"][server_id]["enforce_prefix"] = False
        self.bot.configs["servers"][server_id]["prefix"] = None
