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
        log_message = ":pencil: {0.name}#{0.discriminator} (`{0.id}`) message in {1.channel.mention}\n**B** {1.clean_content}\n**A** {2.clean_content}"
        log_message = log_message.format(before.author,before,after)
        await self.bot.send_message(await self.get_log_channel(before.server.id), log_message)

    async def on_message_delete(self, message):
        if await self.get_log_channel(message.server.id) is None:
            return
        log_message = ":wastebasket: {0.name}#{0.discriminator} (`{0.id}`) message deleted in {1.channel.mention} \n{1.clean_content}".format(message.author, message)
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

    async def on_member_join(self, member):
        if await self.get_log_channel(member.server.id) is None:
            return
        creation = discord.utils.snowflake_time(member.id)
        log_message = ":inbox_tray: {0.name}#{0.discriminator} (`{0.id}`) joined the server (Created {1})".format(member, creation)
        await self.bot.send_message(await self.get_log_channel(member.server.id), log_message)

    async def on_member_remove(self, member):
        if await self.get_log_channel(member.server.id) is None:
            return
        log_message = ":outbox_tray: {0.name}#{0.discriminator} (`{0.id}`) left the server".format(member)
        await self.bot.send_message(await self.get_log_channel(member.server.id), log_message)

    async def on_member_update(self, before, after):
        if before.nick!=after.nick:
            if before.nick is None:
                log_message = ":name_badge: {0} (`{0.id}`) added a nick `{1.nick}`"
            elif after.nick is None:
                log_message = ":name_badge: {0} (`{0.id}`) removed a nick `{0.nick}`"
            else:
                log_message =":name_badge: {0} (`{0.id}`) changed their nick from `{0.nick}` to `{1.nick}`"
        elif before.name != after.name:
            log_message = ":name_badge: {1} (`{0.id}`) changed their username from {0} to {1}"
        elif before.roles != after.roles:
            delta = set(before.roles).symmetric_difference(set(after.roles))
            for role in delta:
                if (role in after.roles):
                    log_message = ":key: {0} (`{0.id}`) added a role {1.name}"
                else:
                    log_message = ":key: {0} (`{0.id}`) removed a role {1.name}"
                await self.bot.send_message(await self.get_log_channel(before.server.id),log_message.format(before,role))
            return
        else:
            return
        await self.bot.send_message(await self.get_log_channel(before.server.id),log_message.format(before,after))
        
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
