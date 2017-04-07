import discord

import config


class Events:
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, message, channel):
        try:
            channel = self.bot.get_channel(config.guilds[message.server.id][channel])
        except KeyError as e:
            channel = self.bot.get_channel(config.guilds[message.server.id]['server-log'])
        finally:
            return channel

    async def on_message(self, message):
        pass

    async def on_message_edit(self, before, after):
        log_message = ":pencil: {0.name}#{0.discriminator} (`{0.id}`) edited their message in {1.channel.mention}\n**B** {1.content}\n**A** {2.content}"
        log_message = log_message.format(before.author,before,after)
        #dont forget to add something for message saving to the DB
        await self.bot.send_message((await self.get_log_channel(before, 'message-log')), log_message)

    async def on_message_delete(self, message):
        log_message = ":wastebasket: {0.name}#{0.discriminator} (`{0.id}`) deleted from channel {1.channel.mention} \n{1.content}".format(message.author, message)
        await self.bot.send_message((await self.get_log_channel(message, 'message-log')), log_message)

def setup(bot):
    bot.add_cog(Events(bot))
