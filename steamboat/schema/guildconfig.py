from mongoengine import *

class GuildConfig(Document):
    ''' Settings specific to a guild '''
    guild = IntField(required=True)
    mod_log = IntField(required=False)
    server_log = IntField(required=False)