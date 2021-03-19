from django.conf.urls import re_path, include

from .views import *

urlpatterns = [
    re_path(r'^car-brand/$',CarBrandView.as_view(),name='car-brand'),
    re_path(r'^car-model/(?P<id>\d+)/$',CarModelView.as_view(),name='car-model'),
    re_path(r'^car-trim/(?P<id>\d+)/$',CarTrimView.as_view(),name='car-trim'),

]
