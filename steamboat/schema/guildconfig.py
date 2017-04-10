from mongoengine import *

class GuildConfig(Document):
    ''' Settings specific to a guild '''
    guild = IntField(required=True)
    log = IntField(required=False)
    mute_role = IntField(required=False)

    async def getGuild(guild):
        ''' Returns a guild config dict '''
        try:
            server = GuildConfig.objects.get(guild=guild).to_mongo().to_dict()
            return server
        except DoesNotExist:
            return None