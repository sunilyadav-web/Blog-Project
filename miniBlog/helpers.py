from requests import request
from Blog import settings
from django.utils.text import slugify
from django.core.mail import send_mail

import string 
import random


def generate_random_string(N):
    res=''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
    return res


def generate_slug(text):
    new_slug=slugify(text)
    from .models import BlogModel
    if BlogModel.objects.filter(slug=new_slug).exists():
        new_slug=generate_slug(text + generate_random_string(5))

    return new_slug
    
def send_mail_to_user(token,email,domain):
    subject="Your account need to be verified"
    message="Hi paste the link to verify account http://"+domain+"verify/"+token
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,from_email,recipient_list, fail_silently=True)

def send_forget_email(token,email,domain):
    status='Error'
    subject="Please Click on link blow to foreget password"
    message="Please Clink on this link to forget password page http://"+domain+"set-new-password/"+token
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,from_email,recipient_list,fail_silently=True)
    status='success'
    return status
def sendMailForEmailVerification(token,email,domain):
    status='error'
    subject='Please Verify your Email by clicking link below'
    message="Click here to verify email http://"+domain+"email-verify/"+token
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,from_email,recipient_list,fail_silently=True)
    status='success'
    return status