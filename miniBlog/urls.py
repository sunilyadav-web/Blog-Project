from django.urls import path,include
from .views import *
from froala_editor import views

urlpatterns = [
    path('',home,name='home'),
    path('login',signin,name='login'),
    path('signup',register,name='register'),
    path('logout',signout,name='signout'),
    path('add-blog',addBlog,name='addblog'),
    path('blog/<slug>',blogDetail,name='blog_detail'),
    path('see-blogs',seeBlogs,name='seeblogs'),
    path('update-blog<slug>',updateBlog,name='updateblog'),
    path('delete-blog<slug>',deleteBlog,name='deleteblog'),
    path('verify/<token>',verify,name='verify'),
    path('profile',profile,name='profile'),
    path('edit-profile',profileUpdate,name='profile_update'),
    path('search',search,name='search'),
    path('<username>',blogPublisher,name='blog_publisher'),
    path('comment-add/<slug>',commentAdd,name='comment_add'),
    path('comment-delete/<id>',commentDelete,name='comment_delete'),
    
]
