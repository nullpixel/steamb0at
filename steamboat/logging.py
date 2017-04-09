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
                # channel = server.objects.get(mod_log) this is broked
                #print(server.objects)
                # print(channel)    
            except DoesNotExist:
                print("Log channel not configured")

    def configureLogging(self, server, mod_log, server_log):
        try:
            guild = guildconfig.GuildConfig(guild=server, mod_log=mod_log, server_log=server_log)
            guild.save()
            print("Log channels setup for {0}".format(server))
        except:
            print("An error occured setting up log channels for {0}".format(server))
        return

