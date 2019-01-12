from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Profile

@receiver(m2m_changed,sender=Profile.followers.through)
def user_followers_changed(sender,instance,**kwargs):
    instance.followers_count = instance.followers.count()
    instance.save()