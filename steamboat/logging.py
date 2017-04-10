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
        server = await GuildConfig.getGuild(server)
        if server is None:
            return None
        chan_id = server['log']
        if chan_id is None:
            return None
        channel = self.bot.get_channel(str(chan_id))
        return channel

    async def configureLogging(self, server, log):
        try:
            guild = GuildConfig(guild=server, log=log).save()
        except:
            raise LoggingException("An error occured whilst setting up the log channel.")
        return

    def actToDict(self, action):
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
            raise LoggingException("An unknown error happened kek")
    
    async def logIncident(self, guild, action, moderator, targetuser, reason):
        act = self.actToDict(action)
        try:
            log = Incident(guild=guild.id, action=action, moderator=moderator.id, target=targetuser.id, reason=reason).save()
            if await self.getLog(guild.id) is None:
                return
            log_message = "{0} {1.name}#{1.discriminator} (`{1.id}`) was {2} by **{3.name}#{3.discriminator}**: `{4}`".format(act['emoji'], targetuser, act['name'], moderator, reason)
            await self.bot.send_message(await self.getLog(guild.id), log_message)
        except Exception as error:
            raise LoggingException("An unknown error occured whilst logging that incident to the database. "+error)
            print("Error logging incident")