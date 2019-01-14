from .models import Action
from django.utils import timezone
import datetime
from django.contrib.contenttypes.models import ContentType


def add_action(user,action,target):
    now = timezone.now()

    last_minute = now - datetime.timedelta(seconds = 60)

    target_ct = ContentType.objects.get_for_model(target)

    similar_actions = Action.objects.filter(user_id = user.id,action = action, object_id =target.id ,time__gte = last_minute,content_type = target_ct)


    if not similar_actions:
        Action.objects.create(user = user, action = action, content_object = target)

    