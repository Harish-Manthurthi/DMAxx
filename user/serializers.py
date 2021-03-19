from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password

from django.utils.crypto import get_random_string

from datetime import datetime, date,timedelta

# from django.contrib.auth.hashers import set_password



class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = User
        fields = '__all__'
        # exclude = ('is_active','groups','user_permissions','password','is_staff','is_admin','is_admin','is_superuser')

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Password fields didn't match."})
    #
    #     return attrs

    def create(self, validated_data):
        print('print data inside of create --->',validated_data)
        # car_model = CarModel.objects.get(id=validated_data['car_model'])
        # account_type = AccountType.objects.get(id=validated_data['account_type'])
        # validated_data['email'] = validated_data['email'].lower()
        user = User.objects.create(email=validated_data['email'].lower(),
            account_type=validated_data['account_type'],
            car_model =validated_data['car_model'],
            car_trim = validated_data['car_trim'],
            date_of_birth = validated_data['date_of_birth'],
            full_name=validated_data['full_name'],
            username=validated_data['username'],
            is_active = False,
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


    def update(self, instance, validated_data):
        # instance.email = validated_data.get('email', instance.email)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.username = validated_data.get('username', instance.username)
        instance.image = validated_data.get('image',instance.image)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance


class ForgetPasswordOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForgetPasswordOTP
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        otp =ForgetPasswordOTP.objects.create(user=validated_data['user'])
        otp.otp = get_random_string(length=5, allowed_chars='0123456789')
        otp.expired_time = otp.created + timedelta(minutes=5)
        print('expired time',otp.expired_time)
        otp.save()

        print('otp serializer --',otp)
        return otp
