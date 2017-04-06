import discord

import config


class Events:
    def __init__(self, bot):
        self.bot = bot
    async def get_log_channel(self, message):
        return self.bot.get_channel(config.guilds[message.server.id]['server-log'])
    
    async def on_message(self, message):
        pass
    
    async def on_message_edit(self, before, after):
        pass
    
    async def on_message_delete(self, message):
        log_message = ":wastebasket: {0.name}#{0.discriminator} (`{0.id}`) deleted from channel {1.channel.mention} \n{1.content}".format(message.author, message)
        await self.bot.send_message((await self.get_log_channel(message)), log_message)


def setup(bot):
    bot.add_cog(Events(bot))