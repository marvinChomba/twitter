from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from pyuploadcare.dj.models import ImageField
from django.dispatch import receiver
from actions.models import Action
from django.db.models.signals import post_save,m2m_changed
from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    bio = models.CharField(max_length=30,default = "Hey there! I'm using twitter")
    pic = ImageField(blank=True,manual_crop="")
    followers = models.ManyToManyField(User,related_name="followers",blank=True)
    following = models.ManyToManyField(User,related_name="following",blank=True)
    followers_count = models.PositiveIntegerField(db_index = True,default=0)
    actions = GenericRelation(Action)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return "Profile for {}".format(self.user.username)

@receiver(m2m_changed, sender=Profile.followers.through)
def users_like_changed(sender, instance, **kwargs):
    instance.followers_count= instance.followers.count()
    instance.save()


User.add_to_class("actions", GenericRelation(Action))





