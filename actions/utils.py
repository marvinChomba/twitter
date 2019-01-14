from .models import Action
from django.utils import timezone
import datetime


def add_action(user,action,target):
    now = timezone.now()

    last_minute = now - datetime.timedelta(seconds = 60)

    similar_actions = Action.objects.filter(user_id = user.id,action = action, content_object = target,time__gte = last_minute)


    if not similar_actions:
        Action.objects.create(user = user, action = action, content_object = target)

    