from mongoengine import *
import datetime

class MessageLog(Document):
    ''' Schema for a message to be logged '''
    guild = IntField(required=True)
    channel = IntField(required=True)
    author = IntField(required=True)
    content = StringField(required=True, max_length=2000)
    timestamp = DateTimeField(default=datetime.datetime.now)
