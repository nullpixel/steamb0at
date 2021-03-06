#!/usr/bin/env python3
from mongoengine import *
import sys
from discord.ext import commands
import steamboat.config as config

init_cogs = ["cogs.admin", "cogs.moderation", "cogs.events"]

bot = commands.Bot(command_prefix=config.bot['prefix'])

@bot.event
async def on_ready():
    print("I'm logged into discord!")

if __name__ == '__main__':
    try:
        connect(config.database['name'], host=config.database['host'], port=config.database['port'])
        print("Connected to database")
    except:
        print("Could not connect to mongodb")

    debug = any('debug' in arg.lower() for arg in sys.argv)
    if debug:
        bot.command_prefix = config.debug_bot['prefix']
        token = config.debug_bot['token']
    else:
        token = config.bot['token']
    
    for cog in init_cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(cog, exc))
    
    bot.run(token)
