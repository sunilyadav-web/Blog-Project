from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from .helpers import *

class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    is_varified=models.BooleanField(default=False)
    token=models.CharField(max_length=100)
    bio=models.TextField(max_length=40, null=True , blank=True, default="this is bio")
    # image=models.ImageField(upload_to='blog',default='../static/img/user.png', null)
    def __str__(self):
        return self.user.first_name

class BlogModel(models.Model):
    title=models.CharField(max_length=1000)    
    content=FroalaField()
    slug=models.SlugField(max_length=1000, null=True,  blank=True)
    image=models.ImageField(upload_to='blog')
    user=models.ForeignKey(User, null=True, blank=True ,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    upload_to=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self,  *args, **kwargs):
        s=generate_slug(self.title)
        print('this is slug',s)
        self.slug=s
        super(BlogModel,self).save(*args, **kwargs)
