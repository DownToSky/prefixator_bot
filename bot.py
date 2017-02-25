import discord
import asyncio
from discord.ext import commands
from utils import assign_prefix

class Bot(commands.Bot):
    def __init__(self, **args):
        self.configs = args["configurations"]
        default_prefix = self.configs["default_prefix"]
        description = self.configs["description"]
        super().__init__(command_prefix = commands.when_mentioned_or(default_prefix), description = description)
        self.TOKEN = args["token"]
        self.EMAIL   = args["email"]
        self.PASSWORD = args["password"]
        if self.TOKEN == None and (self.EMAIL == None or self.PASSWORD == None):
            raise ValueError("A username and password combination or a token combination" 
                                "is required to connect to Discord server")
        extensions = ["core","prefix"]
        for e in extensions:
            self.load_extension("command_groups.{}".format(e))

    async def prefixate_server(self, server, old_prefix = "", new_prefix = "")
        if old_prefix == new_prefix:
            return
        for member in server.members:
            nick = member.name 
            if member.nick is not None:
                nick = member.nick 
                if len(nick) >= len(new_prefix) and nick[:len(new_prefix)] == new_prefix:
                    continue 
                
            new_nick = assign_prefix(nick, new_prefix)

    async def prefixate_server(self, server):
        server_prefix = self.configs["servers"][server.id]["prefix"]
        for member in server.members:
            nick = member.name
            if member.nick is not None:
                nick = member.nick
            new_nick = assign_prefix(nick, server_prefix)
            if len(server_prefix)<= len(nick) and nick[:len(server_prefix)] ==  server_prefix:
                continue
            print("setting the prefix for {}".format(member.name))
            try:
                await self.change_nickname(member, new_nick)
            except:
                pass


    async def prefixate_all_servers(self):
        for server in self.servers:
            if server.id not in self.configs["servers"]:
                self.configs["servers"][server.id] ={
                    "enforce_prefix": False,
                    "prefix": ""
                }
            if self.configs["servers"][server.id]["enforce_prefix"] is True:
                server_prefix = self.configs["servers"][server.id]["prefix"]
                await self.prefixate_server(serveri, new_prefix = server_prefix)

    async def on_ready(self):
        print('Logging in as')
        print(self.user.name.encode('ascii', errors="backslashreplace").decode())
        print(self.user.id.encode("ascii", errors="bachslashreplace").decode())
        print("------------")
        await self.prefixate_all_servers()
        print("Prefixing server members done!")
        

    async def on_message(self, message):
        try:
            await self.process_commands(message)
        except Exception as e:
            print("Command error unhandled")
            print(message.content)
            print(e)
    
    def run(self):
        if self.TOKEN != None:
            super(Bot,self).run(self.TOKEN)
        else:
            super(Bot,self).run(email=self.EMAIL, password=self.PASSWORD)
