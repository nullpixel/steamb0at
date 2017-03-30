from discord.ext import commands
from .utils import checks

class Admin():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(hidden=True)
    @checks.is_owner()
    async def load(extension_name : str):
        """Loads an extension."""
        try:
            self.bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await self.bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await self.bot.say("{} loaded.".format(extension_name))
    
    @commands.command(hidden=True)
    @checks.is_owner()
    async def unload(extension_name : str):
        """Unloads an extension."""
        self.bot.unload_extension(extension_name)
        await self.bot.say("{} unloaded.".format(extension_name))

def setup(bot):
    bot.add_cog(Admin(bot))