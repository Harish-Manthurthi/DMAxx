from rest_framework import serializers
from .models import *

from django.utils.crypto import get_random_string
from datetime import datetime, date,timedelta
from user.serializers import UserSerializer


class PostModelSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = PostModel
        fields = '__all__'


    def create(self, validated_data):
        print(validated_data,'validated data--->')
        post = PostModel.objects.create(user=validated_data['user'],
            title=validated_data['title'],
            message =validated_data['message'],
            image = validated_data['image'],
            visibility = validated_data['visibility'])

        post.save()
        return post
    #
    #
    # def update(self, instance, validated_data):
    #     # instance.email = validated_data.get('email', instance.email)
    #     instance.full_name = validated_data.get('full_name', instance.full_name)
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.image = validated_data.get('image',instance.image)
    #     instance.bio = validated_data.get('bio', instance.bio)
    #     instance.save()
    #     return instance
    #

class PostLikeModelSerializer(serializers.ModelSerializer):
    # user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = PostLikeModel
        fields = '__all__'
        depth = 1 
