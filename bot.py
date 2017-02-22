import discord
import asyncio
from discord.ext import commands

class bot(commands.bot):
    def __init__(self, **args):
        prefix = args["prefix"]
        description = args["description"]
        super().__init__(command_prefix = commands.when_mentioned_or(prefix)
                            ,description = description)
        self.TOKEN = args["token"]
        extensions = args["extensions"]
        for e in extensions:
            self.load_extension("command_groups.{}".format(e))

    def on_ready(self):
        print('Logging in as')
        print(self.user.name.encode('ascii', errors="backslashreplace").decode())
        print(self.user.name.encode("ascii", errors="bachslashreplace").decode())
        print("------------")

    async def on_message(self, message):
        try:
            await self.process_commands(message)
        except Exception as e:
            print("Command error unhandled")
            print(message.content)
            print(e)
    
    def run(self):
        super(bot,self).run(self.TOKEN)
