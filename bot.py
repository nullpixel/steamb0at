#!/usr/bin/env python3
from discord.ext import commands
import sys, config

init_cogs = ["cogs.admin", "cogs.moderation", "cogs.events"]

bot = commands.Bot(command_prefix=config.prefix)

@bot.event
async def on_ready():
    print("I'm logged into discord!")

if __name__ == '__main__':
    debug = any('debug' in arg.lower() for arg in sys.argv)
    if debug:
        bot.command_prefix = config.debug_prefix
        token = config.debug_token
    else:
        token = config.token

    for cog in init_cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(cog, exc))

    bot.run(token)
