from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
import datetime
from django.utils import timezone
import uuid

from car.models import CarModel,CarTrim

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser =True
        user.role = 'admin'
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class AccountType(models.Model):
    type = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.type


class User(AbstractBaseUser,PermissionsMixin):
    user_type = (
    ("admin", "ADMIN"),
    ("normal", "NORMAL"))
    # username = models.CharField(max_length=500,blank=True, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('UserName'),null=True,blank=True,max_length=200)
    full_name = models.CharField(max_length=300,null=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now_add=True)
    mobile = models.CharField(_('Mobile Number'),null=True,max_length=12)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField( max_length = 20, choices = user_type, default = 'normal')
    account_type = models.ForeignKey(AccountType,on_delete=models.CASCADE,null=True,blank=True)
    car_model = models.ForeignKey(CarModel,on_delete=models.CASCADE,null=True,blank=True)
    car_trim = models.ForeignKey(CarTrim,on_delete=models.CASCADE,null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    image = models.ImageField(upload_to ='profile/',blank=True,default='not-Anonymous.png')
    bio = models.CharField(max_length=1000,null=True,blank=True)

    password = models.CharField(max_length=100,blank=True,null=True)
    # address = models.CharField(max_length=100,blank=True,null=True)
    # street = models.CharField(max_length=100,blank=True,null=True)
    # landmark =models.CharField(max_length=100,blank=True,null=True)
    # pincode =models.CharField(max_length=100,blank=True,null=True)

    # bio = models.TextField(blank=True,default="")
    # profile_set_up_flag = models.BooleanField(default=False)


    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
    	return f'{self.email} - ({self.full_name})'

class ProfileActivation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, models.CASCADE, related_name='profile')
    activation_status = models.BooleanField(default=False)
    expired_status = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return f'{self.user} - Activation status - {self.activation_status}'


class ForgetPasswordOTP(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    otp = models.IntegerField(default=0)
    expired_status = models.BooleanField(default=False)
    expired_time = models.DateTimeField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.otp}'
