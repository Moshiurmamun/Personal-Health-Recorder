from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save





class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=18, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    permanent_address = models.CharField(max_length=100, null=True, blank=True)
    present_address = models.CharField(max_length=100, null=True, blank= True)
    image = models.ImageField(upload_to='user_image', null=True, blank=True)


    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
