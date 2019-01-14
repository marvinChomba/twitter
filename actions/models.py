from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation

# Create your models here.
class Action(models.Model):
    user = models.ForeignKey(User,related_name = "actions",on_delete = models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length = 30)
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, related_name="target_obj", on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return "{} {} {}".format(self.user.username,self.action,self.content_object)


