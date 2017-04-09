from discord.ext import commands
from .utils import checks
import discord


class Moderation:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str):
        try:
            await self.bot.kick(member)
        except discord.Forbidden:
            await self.bot.say('I don\'t have permission to do that :frowning:')
        else:
            await self.bot.say(':ok_hand: kicked {0.name}#{0.discriminator} (`{1}`)'.format(member, reason))
    
    @commands.command(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str):
        try:
            await self.bot.ban(member)
        except discord.Forbidden:
            await self.bot.say('I don\'t have permission to do that :frowning:')
        else:
            await self.bot.say(':ok_hand: banned {0.name}#{0.discriminator} (`{1}`)'.format(member, reason))


def setup(bot):
    bot.add_cog(Moderation(bot))