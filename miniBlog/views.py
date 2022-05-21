from django.shortcuts import redirect, render
from .form import *
from django.contrib import messages
from django.contrib.auth import logout

def home(request):
    context={'blogs':BlogModel.objects.all()}
    return render(request,'blog/home.html',context)

def signin(request):
    return render(request,'blog/login.html')

def register(request):
    return render(request,'blog/register.html')

def verify(request, token):
    try:
        profile_obj=Profile.objects.filter(token=token).first()

        if profile_obj:
            profile_obj.is_varified=True
            profile_obj.save()
        return redirect(signin)
    except Exception as e:
        print(e)

def signout(request):
    logout(request)
    return redirect(home)

def profile(request):
    return render(request,'blog/profile.html')

def addBlog(request):
    context={'form':BlogForm}
    try:
        if request.method == 'POST':
            form=BlogForm(request.POST)
            title=request.POST['title']
            image=request.FILES['image']
            user=request.user

            if form.is_valid():
                content=form.cleaned_data['content']
            
            BlogModel.objects.create(user=user, title=title, image=image, content=content)
            messages.SUCCESS(request,'Your Blog Published successfully!')
            context['messages']=messages
            redirect(addBlog)
    except Exception as e :
        print(e)
    
    
    return render(request,'blog/add_blog.html',context)

def blogDetail(request,slug):
    context={}
    try:
        blog_obj=BlogModel.objects.filter(slug=slug).first()
        context['blog_obj']=blog_obj
    except Exception as e:
        print(e)
    return render(request,'blog/blog_detail.html',context)

def seeBlogs(request):
    context={}
    try:
        blog_objs=BlogModel.objects.filter(user=request.user)
        context['blog_objs']=blog_objs
    except Exception as e:
        print(e)
    return render(request,'blog/see_blogs.html' ,context)


def updateBlog(request , slug):
    context={}
    try:
        blog_obj=BlogModel.objects.get(slug=slug)
        if request.user != blog_obj.user:
            return redirect(home)

        initial_dict={'content':blog_obj.content}    
        form=BlogForm(initial=initial_dict)

        if request.method== 'POST':
            form=BlogForm(request.POST)
            image=request.FILES['image']
            title=request.POST['title']
            user=request.user

            if form.is_valid():
                content=form.cleaned_data['content']

            blog_ob=BlogModel.objects.create(user=user,image=image,title=title,content=content)
            

        context['blog_obj'] = blog_obj
        context['form'] = form

        
        
    except Exception as e:
        print(e)

    return render(request,'blog/update_blog.html' ,context)

def deleteBlog(request,slug):
    try:
        blog=BlogModel.objects.get(slug=slug)
        if request.user == blog.user:
            blog.delete()
            return redirect(seeBlogs)
        else:
            return redirect(home)    
    except Exception as e:
        print(e)
    