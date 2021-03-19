from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage, EmailMultiAlternatives
# from django.utils.crypto import get_random_string

from django.conf import settings
import datetime

def send_activation_email(subject, to, link,user):

    subject = subject
    to = [to]
    from_email = settings.EMAIL_HOST_USER
    ctx = {
    	'user':user,
        'email': to,
        'subject': subject,
        'link': link
    }
    print('email cts --',ctx)
    message = render_to_string('email/activation.html',ctx)
    # message ='HI ... '+str(first_name)+' Please check on the below link \n'+str(link)
    msg = EmailMultiAlternatives(subject, to=to, from_email=from_email)
    msg.attach_alternative(message, "text/html")

    # msg.content_subtype = "html"
    msg.send()
    return True

def forget_password_otp_email(subject, to, otp,user):

    subject = subject
    to = [to]
    from_email = settings.EMAIL_HOST_USER
    ctx = {
    	'user':user,
        'email': to,
        'subject': subject,
        'otp': otp
    }
    print('email cts --',ctx)
    message = render_to_string('email/otp-mail.html',ctx)
    # message ='HI ... '+str(first_name)+' Please check on the below link \n'+str(link)
    msg = EmailMultiAlternatives(subject, to=to, from_email=from_email)
    msg.attach_alternative(message, "text/html")

    # msg.content_subtype = "html"
    msg.send()
    return True
