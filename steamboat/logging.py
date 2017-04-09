from mongoengine import *
from steamboat import config
from steamboat.schema import incident, message, guildconfig

class Logging:
    def __init__(self, bot):
        self.bot = bot

    def getLog(self, server, channel):
        if channel == 'mod_log':
            try:
                server = guildconfig.GuildConfig.objects.get(guild=server)
                channel = server.objects.get(mod_log)
                print(channel)
            except DoesNotExist:
                print("Log channel not configured")

    def configureLogging(self, server, mod_log, server_log):
        guild = guildconfig.GuildConfig(guild=server, mod_log=mod_log, server_log=server_log)
        return

