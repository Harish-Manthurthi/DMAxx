from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404


################# Post list ##############


class AllNotificationView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,format=None):
        context = queryset = {}
        user = request.user
        context['data'] = AllNotificationSerializer(AllNotification.objects.filter(user=user),many=True).data
        return Response(context,status=status.HTTP_200_OK)
        # except:
        #     return Response(context,status=status.HTTP_400_BAD_REQUEST)
