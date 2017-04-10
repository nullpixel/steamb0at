from mongoengine import *
from steamboat import config
from steamboat.schema.guildconfig import GuildConfig
from steamboat.schema.incident import Incident
from steamboat.schema.message import MessageLog

class LoggingException(Exception):
    pass

class Logging:
    def __init__(self, bot):
        self.bot = bot

    async def getLog(self, server):
        server = GuildConfig.getGuild(server)
        if server is None:
            return None
        channel = await self.bot.get_channel(server['log'])
        return channel

    async def configureLogging(self, server, log):
        try:
            guild = GuildConfig(guild=server, log=log).save()
        except:
            raise LoggingException("An error occured whilst setting up the log channel.")
        return

    def actToDict(action):
        actdict = {'name': None, 'emoji': None}
        if action == 1:
            actdict['name'] = "kicked"
            actdict['emoji'] = ":boot:"
        elif action == 2:
            actdict['name'] = "banned"
            actdict['emoji'] = ":rotating_light:"
        elif action == 3:
            actdict['name'] = "muted"
            actdict['emoji'] = ":no_mouth:"
        return actdict

    async def logMessage(self, message):
        try:
            log = MessageLog(guild=message.server.id, channel=message.channel.id, author=message.author.id, content=message.clean_content).save()
        except:
            print("Error logging message to db")
    
    async def logIncident(self, guild, action, moderator, targetuser, reason):
        act = self.actToDict(action)
        try:
            log = Incident(guild=guild.id, action=action, moderator=moderator.id, target=targetuser.id, reason=reason).save()
            if await getLog(guild) is None:
                return
            log_message = "{0['emoji']} {1.name}#{1.discriminator} (`{1.id}`) was {0['name']} by **{2.name}#{2.discriminator}**: `{3}`".format(act, targetuser, moderator, reason)
            self.bot.send_message(await getLog(guild), log_message)
        except:
            raise LoggingException("An unknown error occured whilst logging that incident to the database.")
            print("Error logging incident")