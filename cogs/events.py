import discord

import config


class Events:
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self, server_id, channel):
        try:
            channel = self.bot.get_channel(config.guilds[server_id][channel])
        except KeyError:
            channel = self.bot.get_channel(config.guilds[server_id]['server-log'])
        finally:
            return channel

    async def on_message(self, message):
        pass

    async def on_message_edit(self, before, after):
        log_message = ":pencil: {0.name}#{0.discriminator} (`{0.id}`) edited their message in {1.channel.mention}\n**B** {1.clean_content}\n**A** {2.clean_content}"
        #dont forget to add something for message saving to the DB
        log_message = log_message.format(before.author,before,after)
        await self.bot.send_message(await self.get_log_channel(before.server.id, 'message-log'), log_message)

    async def on_message_delete(self, message):
        log_message = ":wastebasket: {0.name}#{0.discriminator} (`{0.id}`) deleted from channel {1.channel.mention} \n{1.clean_content}".format(message.author, message)
        await self.bot.send_message(await self.get_log_channel(message.server.id, 'message-log'), log_message)
        
    async def on_channel_create(self, channel):
        log_message = ":pen_ballpoint: #{0} was created".format(channel.name)
        await self.bot.send_message(await self.get_log_channel(channel.server.id, 'server-log'), log_message)
    
    async def on_channel_delete(self, channel):
        log_message = ":wastebasket: #{0} was deleted".format(channel.name)
        await self.bot.send_message(await self.get_log_channel(channel.server.id, 'server-log'), log_message)

def setup(bot):
    bot.add_cog(Events(bot))
