import discord

class Events():
    def __init__(self, bot):
        self.bot = bot

    async def on_message(message):
        return

def setup(bot):
    bot.add_cog(Events(bot))