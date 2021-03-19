from django.contrib import admin
from .models import *
# Register your models here.
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['user','title','visibility','message','no_of_like','no_of_comments','created','updated']
    search_fields = ['user__full_name','title']
    list_filter = ['user__full_name','visibility']

admin.site.register(PostModel,PostModelAdmin)



class PostLikeModelAdmin(admin.ModelAdmin):
    list_display = ['user','post','like','created','updated']
    search_fields = ['user__full_name','post__user__full_name']
    list_filter = ['user__full_name','post__user__full_name','like']

admin.site.register(PostLikeModel,PostLikeModelAdmin)
