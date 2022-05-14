from django.urls import path,include
from .views import *
from froala_editor import views

urlpatterns = [
    path('',home,name='home'),
    
]
