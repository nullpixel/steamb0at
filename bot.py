#!/usr/bin/env python3
import discord
import sys 
import config

init_cogs = ["cogs.admin", "cogs.moderation", "cogs.events"]

bot = discord.Client()

@bot.event
async def on_ready():
    print("I'm logged into discord!")

@bot.event
async def on_message(message):
    print(message.server.id)

@bot.event
async def on_message_delete(message):
    logChannel = bot.get_channel(config.guilds[message.server.id]['server-log'])
    logMessage = ":wastebasket: "+message.author.name+"#"+message.author.discriminator+"`"+message.author.id+"` deleted from channel #"+message.channel.name+"\n"+message.content
    await bot.send_message(logChannel,logMessage)

if __name__ == '__main__':
    debug = any('debug' in arg.lower() for arg in sys.argv)
    if debug:
        prefix = config.debug_prefix
        token = config.debug_token
    else:
        prefix = config.prefix
        token = config.token

    
    bot.run(token)
