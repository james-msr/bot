from django.db import models
from django.db.models import BooleanField, CharField, ForeignKey


class Channel(models.Model):
    channel_name = CharField('Channel id', max_length=50, default=0)
    is_active = BooleanField(default=True)

    def __str__(self):
        return self.channel_name
    
    def get_profiles(self):
        return self.profile_set.all()
    
    


class Profile(models.Model):
    channel = ForeignKey(Channel, on_delete=models.CASCADE)
    insta = CharField('Instagram accaunt', max_length=50, default=0)
    lastkey_insta = CharField('Last key', max_length=50, default=0)

    def __str__(self):
        return self.insta
    
    def get_lastkeys(self):
        return self.lastkey_set.all()

