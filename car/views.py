from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import *
from .serializers import *

################# car brand ##############

class CarBrandView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request,format=None):
        context = {}
        # try:
        context['data'] = CarBrandSerializer(CarBrand.objects.all(),many=True).data
        # except :
        # return Response(context,status=status.HTTP_400_BAD_REQUEST)

        return Response(context,status=status.HTTP_200_OK)

################ car model ######################
class CarModelView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request,id,format=None):
        context = {}
        try:
            context['data'] = CarModelSerializer(CarModel.objects.filter(brand_id=id),many=True).data
        except :
            return Response(context,status=status.HTTP_400_BAD_REQUEST)

        return Response(context,status=status.HTTP_200_OK)


################ car Trim #############################

class CarTrimView(APIView):
    permission_classes = (AllowAny,)

    def get(self,request,id,format=None):
        context = {}
        try:
            context['data'] = CarTrimSerializer(CarTrim.objects.filter(model_id=id),many=True).data
        except :
            return Response(context,status=status.HTTP_400_BAD_REQUEST)

        return Response(context,status=status.HTTP_200_OK)
