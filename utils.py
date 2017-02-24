import discord
import re
from discord.ext import commands

def assign_prefix(name, prefix):
    MAX_NICK_LEN = 32   
    if len(prefix) > MAX_NICK_LEN:
        raise ValueError("Nickname prefix should not be longer than the"
                            "maximum nickname length")
    if len(prefix)+len(name) <= MAX_NICK_LEN:
        return prefix + name
    else:
        return prefix + name[:len(name)-len(prefix)]

def is_owner(ctx):
    return ctx.message.author.id == ctx.bot.configs["owner_id"]

def is_admin_or_above(cts):
    return is_owner(ctx) or ctx.message.author.server_permissions.kick_members

def find_user(ctx, name):
    user = None
    if re.fullmatch(r"<@![0-9]+>", name):
        user = discord.utils.get(ctx.message.server.members, mention = name)
    elif re.fullmatch(r"[0-9]+", name):
        user = discord.utils.get(ctx.message.server.members, id = name)
    else:
        user = discord.utils.find(lambda m: name.lower() in m.name.lower(), ctx.message.server.members)
    return user
