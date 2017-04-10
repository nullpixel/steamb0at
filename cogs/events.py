import discord
from discord.ext import commands
from steamboat import config
from steamboat.logging import Logging
import traceback

class Events:
    def __init__(self, bot):
        self.bot = bot
        self.log = Logging(self.bot)

    async def get_log_channel(self, server_id):
        return await self.log.getLog(server_id)

    async def on_message(self, message):
        await self.log.logMessage(message)

    async def on_message_edit(self, before, after):
        if before.content == after.content:
            return
        if await self.get_log_channel(before.server.id) is None:
            return
        
        log_message = ":pencil: {0.name}#{0.discriminator} (`{0.id}`) edited their message in {1.channel.mention}\n**B** {1.clean_content}\n**A** {2.clean_content}"
        log_message = log_message.format(before.author,before,after)
        await self.bot.send_message(await self.get_log_channel(before.server.id), log_message)

    async def on_message_delete(self, message):
        if await self.get_log_channel(message.server.id) is None:
            return
        log_message = ":wastebasket: {0.name}#{0.discriminator} (`{0.id}`) deleted from channel {1.channel.mention} \n{1.clean_content}".format(message.author, message)
        await self.bot.send_message(await self.get_log_channel(message.server.id), log_message)
        
    async def on_channel_create(self, channel):
        if await self.get_log_channel(channel.server.id) is None:
            return
        log_message = ":pen_ballpoint: #{0} was created".format(channel.name)
        await self.bot.send_message(await self.get_log_channel(channel.server.id), log_message)
    
    async def on_channel_delete(self, channel):
        if await self.get_log_channel(channel.server.id) is None:
            return
        log_message = ":wastebasket: #{0} was deleted".format(channel.name)
        await self.bot.send_message(await self.get_log_channel(channel.server.id), log_message)

    async def on_command_error(self, exception, ctx):
        if isinstance(exception, commands.CheckFailure):
            return
        if isinstance(exception, commands.CommandNotFound):
            return
        if isinstance(exception, commands.MissingRequiredArgument):
            self.bot.send_message(ctx.message.channel, "You need to specify all the command arguments")
            return
        tb = traceback.format_exception(type(exception), exception, exception.__traceback__)
        print("\n".join(tb))
        
def setup(bot):
    bot.add_cog(Events(bot))
