from webbrowser import get
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.sites.shortcuts import get_current_site
from .models import *
from django.contrib import messages
from .helpers import *


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
 
 


                

    