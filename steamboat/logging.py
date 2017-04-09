from mongoengine import *
import .config
import .schema.incident, .schema.message, .schema.guildconfig

async def getLogChannel(bot, server, channel):
    guildconfig = GuildConfig.object.get(guild=server) 
    if channel == 'mod_log':
        channel = bot.get_channel(guildconfig.mod_log)
        if channel is None:
            return
    elif channel == 'server-log':
        channel = bot.get_channel(guildconfig.server_log)
        if channel is None:
            return
