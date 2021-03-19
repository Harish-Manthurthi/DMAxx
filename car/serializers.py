from rest_framework import serializers
from .models import *



class CarBrandSerializer(serializers.ModelSerializer):
    # car_model = serializers.SerializerMethodField('getCarModel')

    class Meta:
        model = CarBrand
        # fields = ['id','name','car_model']
        fields = '__all__'

    # def getCarModel(self,obj):
    #     return CarModel.objects.filter(brand_id=obj.id).values_list('name',flat=True)
    #

class CarModelSerializer(serializers.ModelSerializer):
    # brand = CarBrandSerializer(many=False)
    brand = serializers.SlugRelatedField(many=False,read_only=True,slug_field='name')

    class Meta:
        model = CarModel
        fields = '__all__'
        depth = 1


class CarTrimSerializer(serializers.ModelSerializer):
    # brand = CarBrandSerializer(many=False)
    model = serializers.SlugRelatedField(many=False,read_only=True,slug_field='name')

    class Meta:
        model = CarTrim
        fields = '__all__'
        depth = 1
