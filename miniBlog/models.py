from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from .helpers import *
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
