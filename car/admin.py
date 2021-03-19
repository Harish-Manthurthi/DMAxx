from django.contrib import admin
from .models import *
# Register your models here.
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1
#
########## car brand ######################

class CarBrandAdmin(admin.ModelAdmin):
    list_display = ['name','active','created_at','updated_at']
    search_fields = ['name']
    list_filter = ['name']
    inlines = [CarModelInline]

admin.site.register(CarBrand,CarBrandAdmin)

############ car model #################

class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name','brand','active','created_at','updated_at']
    search_fields = ['name','brand__name']
    list_filter = ['name','brand__name']
    # inlines = [CarModelInline]

admin.site.register(CarModel,CarModelAdmin)


class CarTrimAdmin(admin.ModelAdmin):
    list_display = ['name','model','active','created_at','updated_at']
    search_fields = ['name','model__name','model__brand__name']
    list_filter = ['name','model__name']
    # inlines = [CarModelInline]

admin.site.register(CarTrim,CarTrimAdmin)
