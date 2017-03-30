from discord.ext import commands
from .utils import checks
import discord

class Moderation():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    @checks.admin_or_permissions(kick_members=True)
    async def kick(self, *, member : discord.Member):
        try:
            await self.bot.kick(member)
        except discord.Forbidden:
            await self.bot.say('I don\'t have permission to do that :frowning:')
        else:
            await self.bot.say('An unhandled error was raised whilst kicking that user.')
    
    @commands.command(no_pm=True)
    @checks.admin_or_permissions(ban_members=True)
    async def ban(self, *, member : discord.Member):
        try:
            await self.bot.ban(member)
        except discord.Forbidden:
            await self.bot.say('I don\'t have permission to do that :frowning:')
        else:
            await self.bot.say('An unhandled error was raised whilst banning that user.')

def setup(bot):
    bot.add_cog(Moderation(bot))