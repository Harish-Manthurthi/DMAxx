from django.db import models
from user.models import User

post_visiablity = (('public','Public'),('only me','Only Me'))
# Create your models here.
class PostModel(models.Model):

    def image_path(instance,filename):
        # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
        return f'{instance.user.id}/{filename}'

    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    title = models.CharField(max_length=200,default="",null=True,blank=True)
    message = models.TextField(blank=True,null=True,default="")
    image = models.FileField(upload_to=image_path,null=True,blank=True)
    visibility=models.CharField(max_length=100,default='Public',choices=post_visiablity,blank=True)
    active = models.BooleanField(default=True)
    no_of_like = models.IntegerField(default=0,blank=True)
    no_of_comments = models.IntegerField(default=0,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.user}'


class PostLikeModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel,on_delete=models.CASCADE)
    like =models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.post}'
