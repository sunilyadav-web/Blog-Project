from django.contrib import admin
from .models import *

admin.site.register(BlogModel)
admin.site.register(Profile)
admin.site.register(CommentModel)
class CommentModelAdmin(admin.ModelAdmin):
    list_display=('user','blog','comment')
admin.site.register(LikeModel)
