from webbrowser import get
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.sites.shortcuts import get_current_site
from .models import *
from django.contrib import messages
from .helpers import *

class LoginView(APIView):
    
    def post(self, request):
        response={}
        response['status']=500
        response['message']='Something went wrong'

        try:
            data=request.data

            if data.get('username') is None:
                response['message']='Key unsername not found'
                raise Exception("Key username not found")

            if data.get('password') is None:
                response['message']='Key Password not found'
                raise Exception('Key Password not found')
            check_user=User.objects.filter(username=data.get('username')).first()

            if check_user is None:
                response['message']='Invalid username not found. Please enter a valid username'
                raise Exception('Invalid username not found. Please enter a valid username')

            user_obj=authenticate(username=data.get('username'),password=data.get('password'))

            if user_obj:
                response['status']=200
                response['message']='Welcome'
                login(request,user_obj)
                messages.success(request,'You are logged in successfully!')
            else:
                response['message']='Incorrect password, Please enter a correct password'
                raise Exception('Incorrect password, Please enter a correct password')
            
        except Exception as e:
            print(e)
        return Response(response)


LoginView=LoginView.as_view()

class RegisterView(APIView):
    
    def post(self,request):
        
        response={}
        response['status']=500
        response['message']='Something went wrong'

        try:
            data=request.data
            
            if data.get('username') is None:
                response['message']='Key username is not none'       
                raise Exception('Key username is not None')

            if data.get('fname') is None:
                response['message']='Key First name not None'
                raise Exception('Key First name not None')

            if data.get('lname') is None:
                response['message']='Key Last not None'
                raise Exception('Key Last name is not None')

            if data.get('email') is None:
                response['message']='Key email not None'
                raise Exception('Key email is not None')
                
            if data.get('password') is None:
                response['message']='Key Password not None'
                raise Exception('Key Password is not None')

            check_user=User.objects.filter(username=data.get('username')).first()

            if check_user:
                response['message']='Username Already Taken'
                raise Exception('Username Already Taken')
                
            

            user_obj=User.objects.create(username=data.get('username'))
            user_obj.set_password(data.get('password'))
            user_obj.first_name=data.get('fname')
            user_obj.last_name=data.get('lname')
            user_obj.email=data.get('email')
            user_obj.save()

            token=generate_random_string(20)
            Profile.objects.create(user=user_obj,token=token)
            email=data.get('email')
            current_site=get_current_site(request)
            send_mail_to_user(token,email,current_site.domain)
            response['message'] = 'User Created sucessfully! Please check your email in order to activate your account'
            response['status'] = 200
            
        except Exception as e:
            print(e)
        
        return Response(response)

RegisterView=RegisterView.as_view()

class GetProfileDataView(APIView):
    def get(self ,request):
        response={}
        response['status']=500
        response['message']='something went wrong'

        try:
            if request.user.is_authenticated:
                profile=Profile.objects.get(user=request.user)
                response['username']=profile.user.username
                response['fname']=profile.user.first_name
                response['lname']=profile.user.last_name
                response['email']=profile.user.email
                response['bio']=profile.bio
                response['status']=200
                response['message']='successful'
        except Exception as e:
            print(e)
        return Response(response)
    
GetProfileDataView=GetProfileDataView.as_view()

class CommentView(APIView):
    def get(slef,request):
        response={}
        response['status']=500
        response['message']='something went wrong'
        try:
            if request.user.is_authenticated:
                
                comment_obj=CommentModel.objects.get(id=request.GET['id'])
                response['comment']=comment_obj.comment
                response['message']='success'
                response['status']=200
        except Exception as e:
            print(e)
        return Response(response)
    
    def post(self,request):
        response={}
        response['status']=500
        response['message']='something went wrong'
        try:
            if request.user.is_authenticated:
                data=request.data
                comment_obj=CommentModel.objects.get(id=data.get('id'))
                comment_obj.comment=data.get('comment')
                comment_obj.save()
                messages.success(request,'Your comment Edited successfully!')
                response['message']='success'
                response['status']=200
        except Exception as e:
            print(e)
        return Response(response)
    
CommentView= CommentView.as_view()

                

    