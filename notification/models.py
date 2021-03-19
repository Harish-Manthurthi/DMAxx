from django.db import models
from user.models import User
from post.models import PostLikeModel


class NotificationType(models.Model):
    type = models.CharField(max_length=200,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type

class AllNotification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    like_notification = models.ForeignKey(PostLikeModel,on_delete=models.CASCADE,null=True,blank=True)
    type = models.ForeignKey(NotificationType,on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
