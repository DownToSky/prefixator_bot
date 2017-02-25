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
        if self.bot.configs["servers"][server_id]["prefixing_done"] == True:
            self.bot.configs["servers"][server_id]["prefixing_done"] = False
        else:
            await self.bot.send_message(ctx.message.channel, "wait until previous prefixing is done!")
            return
        old_prefix = self.bot.configs["servers"][server_id]["prefix"]
        if old_prefix is None:
            old_prefix = ""
        if self.bot.configs["servers"][server_id]["enforce_prefix"] == False:
            self.bot.configs["servers"][server_id]["enforce_prefix"] = True
        self.bot.configs["servers"][server_id]["prefix"] = inputs
        await self.bot.prefixate_server(ctx. message.server,new_prefix = inputs, old_prefix = old_prefix)
        self.bot.configs["servers"][server_id]["prefixing_done"] = True

    @commands.command(name = "removeprefix", pass_context = True)
    async def remove_prefix(self, ctx):
        server_id = ctx.message.server.id
        if self.bot.configs["servers"][server_id]["prefix"] == None:
            await self.bot.send_message(ctx.message.channel, "prefixing on this server is off. Turn it on!")
            return
        if self.bot.configs["servers"][server_id]["prefixing_done"] == True:
            self.bot.configs["servers"][server_id]["prefixing_done"] = False
        else:
            await self.bot.send_message(ctx.message.channel, "wait until previous prefixing is done!")
            return
        old_prefix = self.bot.configs["servers"][server_id]["prefix"]
        await self.bot.prefixate_server(ctx.message.server, old_prefix = old_prefix)
        self.bot.configs["servers"][server_id]["enforce_prefix"] = False
        self.bot.configs["servers"][server_id]["prefix"] = None
        self.bot.configs["servers"][server_id]["prefixing_done"] = True
