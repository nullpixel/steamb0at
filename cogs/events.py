import discord

import config


class Events:
    def __init__(self, bot):
        self.bot = bot
    async def get_log_channel(self, message):
        return self.bot.get_channel(config.guilds[message.server.id]['server-log'])
    
    async def on_message(self, message):
        print(message.server.id)
    
    async def on_message_edit(self, before, after):
        pass
    
    async def on_message_delete(self, message):
        log_message = ":wastebasket: " + message.author.name + "#" + message.author.discriminator + "`" + message.author.id + "` deleted from channel #" + message.channel.name + "\n" + message.content
        await self.bot.send_message((await self.get_log_channel(message)), log_message)


def setup(bot):
    bot.add_cog(Events(bot))