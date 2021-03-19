from django.contrib import admin
from .models import  *
# Register your models here.
class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ['type']

admin.site.register(NotificationType,NotificationTypeAdmin)

class AllNotificationAdmin(admin.ModelAdmin):
    list_display = ['user','like_notification','type','created','updated']
    search_fields = ['user__full_name','like_notification__user__full_name']
    list_filter = ['user__full_name','like_notification__user__full_name']

admin.site.register(AllNotification,AllNotificationAdmin)
