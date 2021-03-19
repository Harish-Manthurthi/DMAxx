from django.conf.urls import re_path, include

from .views import *

urlpatterns = [
    re_path(r'^post/$',PostView.as_view(),name='post'),
    re_path(r'^post-like/(?P<id>\d+)/$',PostLikeView.as_view(),name='post-like'),


]
