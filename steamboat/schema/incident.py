from mongoengine import *
import datetime

class Incident(Document):
    ''' Schema for a moderator action, e.g kick or ban '''
    guild = IntField(required=True)
    # 1: kick
    # 2: ban
    # 3: mute
    action = IntField(required=True)
    moderator = IntField(required=True)
    target = IntField(required=True)
    reason = StringField(required=True)
    timestamp = DateTimeField(default=datetime.datetime.now)
