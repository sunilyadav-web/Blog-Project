from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from .models import Profile
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
                response['message']='invalid username not found'
                raise Exception('invalid username not found')

            user_obj=authenticate(username=data.get('username'),password=data.get('password'))

            if user_obj:
                response['status']=200
                response['message']='Welcome'
                login(request,user_obj)

            else:
                response['message']='Invalid Password'
                raise Exception('invalid Password')
            
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
                
            # if not Profile.objects.filter(user=check_user).first().is_varified:
            #     response['message']='Your Profile is not verified '
            #     raise Exception('Profile not verified')

            user_obj=User.objects.create(username=data.get('username'))
            user_obj.set_password(data.get('password'))
            user_obj.first_name=data.get('fname')
            user_obj.last_name=data.get('lname')
            user_obj.email=data.get('email')
            
            user_obj.save()
            token=generate_random_string(20)
            Profile.objects.create(user=user_obj,token=token)
            send_mail_to_user(token,data.get('email'))
            response['message'] = 'User Created'
            response['status'] = 200
            
        except Exception as e:
            print(e)
        
        return Response(response)

RegisterView=RegisterView.as_view()

    