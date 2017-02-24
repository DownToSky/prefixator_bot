import discord
import asyncio
from discord.ext import commands
import json
import os
import aiohttp
import utils
 
def setup(bot):
    bot.add_cog(Core(bot))
    print("{} module loaded".format(__file__))

class Core:
    def __init__(self,bot):
        self.bot=bot
        bot.loop.create_task(self.update_config_file_task())
        self.bot_session=aiohttp.ClientSession(loop=self.bot.loop)
 
     #Owner only
    @commands.command(name="echo",pass_context=True,hidden=True)
    @commands.check(utils.is_owner)
    async def echo(self,ctx,*,inputs:str):
        await self.bot.say(inputs)
 
    #Owner only
    @commands.command(name="name",pass_context=True,hidden=True)
    @commands.check(utils.is_owner)
    async def change_name(self,ctx,*,new_name:str):
        try:
            await self.bot.edit_profile(username=new_name)
        except:
            await self.say("Error in trying to change bot name")
 
    #Owner only
    @commands.command(pass_context=True,hidden=True)
    @commands.check(utils.is_owner)
    async def avatar(self,ctx):
        url=""
        if ctx.message.attachments:
            url=ctx.message.attachments[0]["url"]
        else:
            await self.bot.say("You must upload an .jpg or .png file while "\
                                 "using this command")
            return
        try:
            with aiohttp.Timeout(8):
                async with self.bot_session.get(url) as response:
                    avatar=await response.read()
                    await self.bot.edit_profile(avatar=avatar)
                    await self.bot.say("Avatar changed")
        except discord.InvalidArgument:
            await self.bot.say("Image was not in .jpg or .png format. "\
                                 "Avatar changing failed.")
        except discord.HTTPException:
            await self.bot.say("HTTP request for the new avatar failed.\n"
                                 "Try again.")
 
    @commands.command(name="userinfo",pass_context=True,no_pm=True)
    async def user_info(self,ctx,name):
        user=utils.find_user(ctx,name)
        if user==None:
            await self.bot.say("`{}` was not found in `{}`\n"
                                 "Try mentioning (write `@<name of user>`"
                                 " or use the user's id)"\
                                 .format(name,ctx.message.server)
                                 )
            return
        else:
            fmt="name: {0.name}\n"\
                 "id: {0.id}\n"\
                 "nick: {nick}\n"\
                 "status: {0.status}\n"\
                 "game: {game}\n"\
                 "avatar url: https://discordapp.com/api/users/{0.id}/avatars/{0.avatar}.jpg"
            nick="`no nicknames`" if user.nick==None else user.nick
            game="`no games`" if user.game==None else user.game.name
 
            await self.bot.say(fmt.format(user,nick=nick ,game=game))
 
     #Usable by owner only
    @commands.command(pass_context=True,hidden=True)
    @commands.check(utils.is_owner)
    async def gameplaying(self,ctx,*,game:str):
        self.bot.configs["game_playing"]=game
        await self.bot.change_status(discord.Game(name=game.strip()))
 
    @commands.command(no_pm=True)
    async def prefix(self):
        await self.bot.say("Current command prefix is:`{}`".format(self.bot.configs["prefix"]))
 
 #Usable by owner only
    @commands.command(pass_context=True,hidden=True)
    @commands.check(utils.is_owner)
    async def die(self,ctx):
        await self.bot.logout()
 
    async def update_config_file_task(self):
         #this should change to a separate thread.
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            path=os.path.join("configurations.json")
            with open(path,'w',encoding="utf-8") as f:
                json.dump(self.bot.configs,f, indent=4, sort_keys=True)
            await asyncio.sleep(60)

