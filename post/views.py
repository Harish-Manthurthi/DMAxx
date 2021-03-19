from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import *
from notification.models import *
from .serializers import *
from django.shortcuts import get_object_or_404


################# Post list ##############


class PostView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,format=None):
        context = queryset = {}
        user = request.user
        # try:
        public_post =PostModel.objects.filter(active=True,visibility='public')
        only_me_post =PostModel.objects.filter(active=True,user=user,visibility='only me')
        combine = public_post.union(only_me_post)
        context['data'] = PostModelSerializer(combine.order_by('-created'),many=True).data
        for i in context['data']:
            print('post data ',i)
            i['like'] = PostLikeModel.objects.filter(user=user,post_id=i['id'],like=True).exists()

        return Response(context,status=status.HTTP_200_OK)
        # except:
        #     return Response(context,status=status.HTTP_400_BAD_REQUEST)

    def post(self,request,format=None):
        context = queryset = {}
        data = request.data
        user = request.user
        data['user']= user.id
        print("data -->",data)
        serializer = PostModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            context['message'] = 'post saved successfully'
            return Response(context,status=status.HTTP_200_OK)
        else:
            context['message'] = "unable to save data"
            context['error'] = serializer.errors
            return Response(context,status=status.HTTP_400_BAD_REQUEST)


################ Post like #######################################


class PostLikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,id,format=None):
        context = {}
        user = request.user
        # try:
        post = get_object_or_404(PostModel, id=id)
        check_post_like = PostLikeModel.objects.filter(user=user,post = post)
        if check_post_like.exists():
            post_like = check_post_like.last()
            if post_like.like:
                post_like.like = False
                context['message'] = 'Post is dislike'
            else:
                post_like.like = True
                context['message'] = 'Post is like'
            post_like.save()
        else:
            like=PostLikeModel.objects.create(user=user,post = post,like=True)
            context['message'] = 'Post is like'

            obj,created = NotificationType.objects.get_or_create(type='like')

            AllNotification.objects.create(user=post.user,like_notification=like,type_id=obj.id)

        return Response(context,status=status.HTTP_200_OK)
        # except :
        #     context['message'] = 'error while post like'
        #     return Response(context,status=status.HTTP_400_BAD_REQUEST)
