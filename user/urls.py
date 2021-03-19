from django.conf.urls import re_path, include

from .views import *

urlpatterns = [
    re_path(r'^account-type',AccountTypeView.as_view(),name='account-type'),

    re_path(r'^login/$', UserLoginView.as_view(),name='login'),
    re_path(r'^user-info/$', UserDetails.as_view(),name='user-info'),

    re_path(r'^username-check/$',UserNameCheck.as_view(),name='username-check'),
    re_path(r'^user-registration/$',UserRegistration.as_view(),name='user-registration'),
    re_path(r'^profile-update/$',ProfileEditView.as_view(),name='profile-update'),

   re_path(r'^activation-link/(?P<key>[0-9a-f-]+)/$',Activation,name='activation-link'),
   re_path(r'^resend-activation-link/(?P<key>[0-9a-f-]+)/$',ReSendActivationEmail,name='resend-activation-link'),

   ############## otp url ####################

   re_path(r'^forget-password-otp/$',ForgetPasswordOTPView.as_view(),name='forget-password-otp'),
   re_path(r'^forget-password-otp-verification/$',ForgetPasswordOTPVerificationView.as_view(),name='forget-password-otp-verification'),
   re_path(r'^password-reset/$',PasswordResetView.as_view(),name='password-reset'),

]
