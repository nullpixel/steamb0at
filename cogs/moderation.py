from discord.ext import commands
from .utils import checks
from steamboat.logging import Logging
from steamboat.logging import LoggingException
import discord


class Moderation:
    def __init__(self, bot):
        self.bot = bot
        self.log = Logging(self.bot)
    
    @commands.command(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str):
        try:
            await self.bot.kick(member)
        except discord.Forbidden:
            await self.bot.say('I don\'t have permission to do that :frowning:')
        else:
            await self.bot.say(':ok_hand: kicked {0.name}#{0.discriminator} (`{1}`)'.format(member, reason))
            try:
                await self.log.logIncident(ctx.message.server, 1, ctx.message.author, member, reason)
            except LoggingException as error:
                await self.bot.say(error)
    
    @commands.command(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str):
        try:
            await self.bot.ban(member)
        except discord.Forbidden:
            await self.bot.say('I don\'t have permission to do that :frowning:')
        else:
            await self.bot.say(':ok_hand: banned {0.name}#{0.discriminator} (`{1}`)'.format(member, reason))
            try:
                await self.log.logIncident(ctx.message.server, 2, ctx.message.author, member, reason)
            except LoggingException as error:
                await self.bot.say(error)

    @commands.command(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def setlog(self, ctx, *, channel: discord.Channel):
        try:
            await self.log.configureLogging(ctx.message.server.id, channel.id)
            await self.bot.say(':ok_hand: I will now log all events to #{0}'.format(channel))
        except LoggingException as error:
            await self.bot.say(error)

def setup(bot):
    bot.add_cog(Moderation(bot))
