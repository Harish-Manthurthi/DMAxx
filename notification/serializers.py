from rest_framework import serializers
from .models import *

from user.serializers import UserSerializer


class AllNotificationSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(many=False,read_only=True,slug_field='type')
    class Meta:
        model = AllNotification
        fields = '__all__'
        depth = 2

#
# class LikeNotificationSerializer(serializers.ModelSerializer):
#     # user = UserSerializer(many=False, read_only=True)
#     class Meta:
#         model = Like
#         fields = '__all__'
#         depth = 1
