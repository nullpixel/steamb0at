from discord.ext import commands
from .utils import checks

class Admin:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(hidden=True)
    @checks.is_owner()
    async def load(self, extension_name: str):
        """Loads an extension."""
        try:
            self.bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await self.bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await self.bot.say("{} loaded.".format(extension_name))
    
    @commands.command(hidden=True)
    @checks.is_owner()
    async def unload(self, extension_name: str):
        """Unloads an extension."""
        self.bot.unload_extension(extension_name)
        await self.bot.say("{} unloaded.".format(extension_name))

    @commands.command(name='reload', hidden=True)
    @checks.is_owner()
    async def _reload(self, *, module : str):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say('\N{PISTOL}')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\N{OK HAND SIGN}')
    
    @commands.command(hidden=True)
    @checks.is_owner()
    async def setting(self, *, type: str, setting: str, value: str):
        return

def setup(bot):
    bot.add_cog(Admin(bot))