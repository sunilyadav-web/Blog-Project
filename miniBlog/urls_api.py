from django.urls import path,include
from .views_api import *

urlpatterns = [
    path('get-profile',GetProfileDataView),
    path('get-comment',CommentView),
    path('update-comment',CommentView),
    
]
