from django.contrib import admin
from user.models import *
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django import forms


admin.site.unregister(Group)

admin.site.site_header = 'DMAXX'
admin.site.site_title = 'DMAXX'
admin.site.index_title = 'DMAXX'


class UserAdmin(admin.ModelAdmin):
    list_display = ("full_name","email","role","mobile","last_login",'updated','created')
    list_filter = ['role','full_name']
    search_fields = ["full_name","role","email","mobile"]
    date_hierarchy = 'created'
    # exclude = ['groups','user_permissions','is_admin','is_staff','is_superuser']
    extra = 1

    def save_model(self, request, obj, form, change):
        # print(obj.type.percentage)
        if str(obj.password).find('pbkdf2_sha256') != -1:
            print("password  match with pbdk2")
            pass
        else:
            print("password not match with pbdk2")
            obj.password = make_password(obj.password)
        obj.save()

admin.site.register(User, UserAdmin)

admin.site.register(ProfileActivation)

admin.site.register(AccountType)


admin.site.register(ForgetPasswordOTP)
