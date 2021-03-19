from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt import views as jwt_views

from datetime import datetime, date
from django.utils import timezone

# from rest_framework_jwt.settings import api_settings
#
# JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
# JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

import requests

from .models import *
from .serializers import *
from .utils import *

################# Genearating JWT Token ###################
def GenerateToken(user,context):
	try:
		# update_last_login(None, user)
		token = RefreshToken.for_user(user)
		# print('token is --',token)
		context['token'] = {}
		context['token']['refresh'] = str(token)
		context['token']['access']  =  str(token.access_token)
		status_code = status.HTTP_200_OK
	except:
		status_code = status.HTTP_400_BAD_REQUEST
		context['error'] = 'Unable to Create Token'

		return status_code


################# login view #########################


class UserLoginView(APIView):
	permission_classes = (AllowAny,)

	def post(self, request, format=None):
		context = {}
		print("user login Api is called ")
		try:
			email = request.data['email'].lower()
			password = request.data['password']
		except:
			context['error'] = "Required parameter not fund. parameter are - email, password"
			return Response(context,status=status.HTTP_400_BAD_REQUEST)

		user_check = User.objects.filter(email__icontains=email)

		if user_check.exists():
			user = user_check.last()

			if user.is_active:
				user = authenticate(request,email=email, password=password)
				if user is None or user == False:
					context['error'] = "invalid user credentials"
					return Response(context,status=status.HTTP_400_BAD_REQUEST)
				else:
					login(request, user)
					context['message'] = 'User successfully Login'
					context['data'] = UserSerializer(user,many=False).data

					status_code=GenerateToken(user,context)

					return Response(context,status=status_code)
			else:
				context['error'] = 'Your account has not yet been activated'
				return Response(context,status=status.HTTP_400_BAD_REQUEST)
		else:
			context['error'] = 'User account is not found '
			return Response(context,status=status.HTTP_400_BAD_REQUEST)

################ User Details #######################

class UserDetails(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request, format=None):
		context = {}
		user = request.user
		context['user'] = UserSerializer(user,many=False).data

		return Response(context,status=status.HTTP_200_OK)


############### Account type #############################

class AccountTypeView(APIView):
	permission_classes = (AllowAny,)

	def get(self,request,format=None):
		context = {}
		try:
			context['data'] = AccountTypeSerializer(AccountType.objects.all(),many=True).data
			# context['car_model'] = CarModelSerializer(CarModel.objects.all(),many=True).data
		except :
			return Response(context,status=status.HTTP_400_BAD_REQUEST)

		return Response(context,status=status.HTTP_200_OK)

############### Registartion #############################

def ActivationLink(request,user):
	token = ProfileActivation.objects.create(user=user)
	domain = request.scheme +'://'+request.META['HTTP_HOST']
	link = f'{domain}/user/activation-link/{token.id}/'
	try:
		send_activation_email("Account Activation DMaxx-250",user.email, link,user.full_name)
		return True
	except:
		return False


class UserNameCheck(APIView):
	permission_classes = (AllowAny,)

	def post(self,request,format=None):
		context = {}
		data = request.data

		user_check = User.objects.filter(username=data['username'])
		if user_check.exists():
			context['error'] = 'Username already exists.'
			return Response(context,status=status.HTTP_400_BAD_REQUEST)
		else:
			context['message'] = 'Username not exists'
			return Response(context,status=status.HTTP_200_OK)

class UserRegistration(APIView):
	permission_classes = (AllowAny,)

	def post(self,request,format=None):
		context ={}
		data = request.data
		print('registration data --',data)
		user_check = User.objects.filter(email__icontains= data['email'].lower())
		if user_check.exists():
			context['error'] = 'User already exists with this email ID '
			return Response(context,status=status.HTTP_400_BAD_REQUEST)
		else:
			username_check = User.objects.filter(username=data['username'])
			if username_check.exists():
				context['error'] = 'Username already exists.Please try different username.'
				return Response(context,status=status.HTTP_400_BAD_REQUEST)
			else:
				serializer = UserSerializer(data=data)
				if serializer.is_valid():
					user = serializer.save()
					print('user --->',user)
					if ActivationLink(request,user):
						context['message'] = 'user created successfully'
						return Response(context,status=status.HTTP_200_OK)
					else:
						context['message'] = 'unable to send email.'
						return Response(context,status=status.HTTP_400_BAD_REQUEST)
				else:
					print('error while saving data ')
					print(serializer.errors)
					context['error'] = serializer.errors
					return Response(context,status=status.HTTP_400_BAD_REQUEST)
		# return Response(context,status=status.HTTP_400_BAD_REQUEST)



def Activation(request, key):
	context = {}
	if request.method == 'GET':
		print("key is:", key)
		profile = ProfileActivation.objects.filter(id=key)
		if profile.exists():
			print("profile key is exists")
			profile = profile.last()
			user = profile.user
			expired_time = profile.created + datetime.timedelta(hours=2)
			current_time = timezone.now()
			print(current_time > expired_time)
			if profile.expired_status or current_time > expired_time:
				profile.expired_status = True
				domain = request.scheme +'://'+request.META['HTTP_HOST']
				link = f'{domain}/user/resend-activation-link/{profile.id}/'
				context['link'] = link
				context['user'] = user
				profile.save()
				return render(request,'email/link-expired.html',context)
			else:
				if user.is_active:
					context['user'] = user.full_name
					profile.expired_status = True
					profile.save()
					print("user account is active")
					return render(request, "email/your-email-has-been-verified.html",context)
				else:
					print("profile is not active")
					profile.activation_status = True
					profile.expired_status = True
					profile.save()
					user.is_active = True
					context['user'] = user.full_name
					user.save()
					return render(request, 'email/your-email-has-been-verified.html',context)
		else:
			return render(request,'404.html')


def ReSendActivationEmail(request,key):
	context = {}
	print("key is:", key)
	profile = ProfileActivation.objects.filter(id=key)
	if profile.exists():
		print("profile key is exists")
		profile = profile.last()
		user = profile.user
		ActivationLink(request,user)
		context['user'] = user.full_name
		return render(request,'email/new-activation.html',context)
	else:
		return render(request,'404.html')


################ Forget password with otp #######################


class ForgetPasswordOTPView(APIView):
	permission_classes = (AllowAny,)

	def post(self,request,format=None):
		context = {}
		email = request.data['email']

		account_check = User.objects.filter(email__icontains=email)

		if account_check.exists():
			user = account_check.last()
			if user.is_active:
				serializer = ForgetPasswordOTPSerializer(data={'user':user.id})
				if serializer.is_valid():
					data = serializer.save()
					forget_password_otp_email('DMaxx250 - Forget Password OTP ', data.user.email, data.otp,data.user.full_name)
					context['message'] = 'OTP send successfully. please check your email.'
					return Response(context,status=status.HTTP_200_OK)
				else:
					print(serializer.errors)
					context['error'] = 'error while generating otp'
					return Response(context,status=status.HTTP_400_BAD_REQUEST)
			else:
				context['error'] = 'Account with this email is not active.'
				return Response(context,status=status.HTTP_400_BAD_REQUEST)
		else:
			context['error'] = 'Account not exist with this email.'
			return Response(context,status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordOTPVerificationView(APIView):
	permission_classes = (AllowAny,)

	def post(self,request,format=None):
		context = {}
		email = request.data['email']
		otp = request.data['otp']
		check_otp = ForgetPasswordOTP.objects.filter(user__email__icontains=email,otp=otp,expired_status=False)
		if check_otp.exists():
			otp = check_otp.last()
			current_time = timezone.now()
			if otp.expired_status or current_time > otp.expired_time :
				otp.expired_status = True
				otp.save()
				context['error'] = 'OTP Expired'
				return Response(context,status=status.HTTP_400_BAD_REQUEST)
			else:
				context['message'] = 'OTP Validate successfully'
				otp.expired_status = True
				otp.save()
				return Response(context,status=status.HTTP_200_OK)
		else:
			context['error'] ='Invalid OTP'
			return Response(context,status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
	permission_classes = (AllowAny,)

	def post(self,request,format=None):
		context = {}
		email = request.data['email']
		new_password = request.data['new_password']
		conf_password = request.data['conf_password']


		account_check = User.objects.filter(email__icontains=email)
		if account_check.exists():
			user = account_check.last()
			if conf_password == new_password:
				user.set_password(new_password)
				user.save()
				context['message'] = 'Password successfully changed.'
				return Response(context,status=status.HTTP_200_OK)
			else:
				context['error'] = 'New password and confirm password does not match'
				return Response(context,status=status.HTTP_400_BAD_REQUEST)
		else:
			context['error'] = 'Account with given email is not exist.'
			return Response(context,status=status.HTTP_400_BAD_REQUEST)

################### Profile Edit ################################

#
class ProfileEditView(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self,request,format=None):
		context = {}
		data = request.data
		user = request.user
		print('profile - update =>',data)
		# image = data.pop('image')
		# data['email'] = user.email
		# data['password'] = user.password
		serializer = UserSerializer(user,data=data,partial=True)
		if serializer.is_valid():
			data =serializer.save()
			# data.image = image
			# data.save()
			context['message'] ="profile data update successfully"
		else:
			print(serializer.errors)
			context['error'] = serializer.errors

		return Response(context)
