from tkinter import E
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .form import *
from django.contrib import messages
from django.contrib.auth import logout,login,authenticate
from django.core.paginator import Paginator
from django.urls import reverse_lazy,reverse
from django.contrib.sites.shortcuts import get_current_site
from .helpers import *


def home(request):
    try:
        blogs = BlogModel.objects.all().order_by('id')
        paginator = Paginator(blogs, 3)
        pages = paginator.page_range
        pageNumber = request.GET.get('page')
        finalBlogpage = paginator.get_page(pageNumber)
        context = {'blogs': finalBlogpage, 'pages': pages}
        profile = Profile.objects.get(user=request.user)
        verify = profile.is_varified
        if not verify:
            messages.warning(request, 'Please verify your Account!')
    except Exception as e:
        print(e)
    return render(request, 'blog/home.html', context)


def signin(request):
    try:
        if request.user.is_authenticated:
            messages.error(request, "You already Logged in!")
            return redirect(home)
        else:
            if request.method == 'POST':
                username=request.POST['username']
                password=request.POST['password']
                
                if username == '':
                    messages.error(request,'Username is must')
                    return redirect(signin) 

                if password == '':
                    messages.error(request,'Password is must')
                    return redirect(signin) 
                check_user=User.objects.filter(username=username).first()
                if check_user is None:
                    messages.error(request,'Invalid username not found. Please enter a valid username.')
                    return redirect(signin)
                user_obj=authenticate(username=username,password=password)
                if user_obj:
                    login(request,user_obj)
                    messages.success(request,'You are logged in successfully!')
                    return redirect(home)
                else:
                    messages.error(request,'Please enter a right credentials!')
    except Exception as e:
        print(e)
    return render(request, 'blog/signin.html')

def checkUsername(request):
    user_obj=User.objects.filter(username=request.GET['username'])
    print('printing username'+request.GET['username'])
    if not user_obj:
        return HttpResponse('true')

def register(request):
    if request.user.is_authenticated:
        messages.error(request, "Please logout then you can Signup!")
        return redirect(home)
    else:
        return render(request, 'blog/register.html')


def verify(request, token):
    try:
        profile_obj = Profile.objects.filter(token=token).first()

        if profile_obj:
            profile_obj.is_varified = True
            profile_obj.save()
        return redirect(signin)
    except Exception as e:
        print(e)

def forgetPassword(request):
    try:
        print('try block')
        if request.method == 'POST':
            print('printing inside post')
            email=request.POST['email']
            current_site=get_current_site(request)
            token=generate_random_string(20)
            user_obj=User.objects.get(email=email)
            profile_obj=Profile.objects.get(user=user_obj)
            profile_obj.token=token
            profile_obj.save()
            status=send_forget_email(token,email,current_site.domain)
            if status =='success':
                messages.success(request,'We have sent you email. Please check that out!')
            
            return redirect(forgetPassword)
    except Exception as e:
        print(e)
    return render(request,'blog/forget_password.html')
def setNewPassword(request,token):
    try:
        context={}        
        profile_obj=Profile.objects.filter(token=token).first()
        if profile_obj:
            user_obj=User.objects.get(username=profile_obj.user.username)
            context['user']=user_obj
            return render(request,'blog/set_new_password.html',context)
    except Exception as e:
        print(e)
    return HttpResponse("Bade request 404")

def saveForgetPassword(request):
    try:
        if request.method == 'POST':
            username=request.POST['username']
            new_password=request.POST['new_password']
            confirm_password=request.POST['confirom_password']
            user_obj=User.objects.get(username=username)
            if confirm_password == new_password:
                print(new_password)
                user_obj.password=new_password
                user_obj.save()
                print(user_obj.password)
                messages.success(request,'Your Password has been changed succfully!')
                return redirect(signin)
            else:
                messages.error(request,'Please enter Both same password')
    except Exception as e:
        print(e)
    return HttpResponse('Bad request 404')

def signout(request):
    try:
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'You are logged out successfully!')
            return redirect(home)
        else:
            messages.error(request, "Please Login!")
            return redirect(signin)
    except Exception as e:
        print(e)
        messages.error(request, 'something went wrong')
        return redirect(home)


def profile(request):
    try:
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            blogs = BlogModel.objects.filter(user=request.user)
            context = {}
            context['blogs'] = blogs
            context['profile'] = profile
            return render(request, 'blog/profile.html', context)
        else:
            messages.error(request, "Please Login!")
            return redirect(home)
    except Exception as e:
        print(e)


def profileUpdate(request):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                user = User.objects.get(username=request.user.username)
                profile_obj = Profile.objects.get(user=request.user)
                username = request.POST['username']
                fname = request.POST['fname']
                lname = request.POST['lname']
                email = request.POST['email']
                bio = request.POST['bio']

                if username:
                    user.username = username

                if fname:
                    user.first_name = fname

                if lname:
                    user.last_name = lname

                if email:
                    user.email = email

                if request.FILES.get('avatar'):
                    profile_obj.avatar = request.FILES['avatar']

                if len(bio) > 150:
                    messages.error(
                        request, "Bio lenght can not be more than 150 characters")
                    raise Exception(
                        'Bio lenght can not be more than 150 characters')

                if bio:
                    profile_obj.bio = bio

                user.save()
                profile_obj.save()
                messages.success(
                    request, 'Your profile has been updated successfully!')
        else:
            messages.error(request, "Please Login!")
            return redirect(home)
    except Exception as e:
        print(e)

    return redirect(profile)


def addBlog(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        verify = profile.is_varified
        if not verify:
            messages.error(
                request, "You can't add blog because Your account is not verified. Please verify!")
            return redirect(home)

        context = {'form': BlogForm}
        try:
            if request.method == 'POST':
                form = BlogForm(request.POST)
                title = request.POST['title']
                image = request.FILES['image']
                user = request.user

                if form.is_valid():
                    content = form.cleaned_data['content']

                BlogModel.objects.create(
                    user=user, title=title, image=image, content=content)
                messages.success(request, 'Your Blog Published successfully!')
                redirect(addBlog)
        except Exception as e:
            print(e)
        return render(request, 'blog/add_blog.html', context)
    else:
        messages.error(request, "Please Login!")
        return redirect(home)


def blogDetail(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug=slug).first()
        comments_obj=CommentModel.objects.filter(blog=blog_obj)
        liked=False
        if blog_obj.likes.filter(id=request.user.id).exists():
            liked=True
        else:
            liked=False
        context['blog_obj'] = blog_obj
        context['comments_obj'] = comments_obj
        context['liked'] = liked
        
    except Exception as e:
        print(e)
    return render(request, 'blog/blog_detail.html', context)


def blogPublisher(request, username):
    context={}
    try:
        user_obj = User.objects.get(username=username)
        if request.user.username == username:
            return redirect(profile)

        blogs = BlogModel.objects.filter(user=user_obj)
        profile_obj = Profile.objects.get(user=user_obj)
        followed=False
        if profile_obj.follower.filter(id=request.user.id):
            followed=True
        else:
            followed=False
        context = {'profile': profile_obj, 'blogs': blogs,'followed':followed}
    except Exception as e:
        print(e)

    return render(request, 'blog/public_profile.html', context)


def seeBlogs(request):
    if request.user.is_authenticated:
        context = {}
        try:
            blog_objs = BlogModel.objects.filter(user=request.user)
            context['blog_objs'] = blog_objs
        except Exception as e:
            print(e)
        return render(request, 'blog/see_blogs.html', context)
    else:
        messages.error(request, "Please Login!")
        return redirect(home)


def updateBlog(request, slug):
    if request.user.is_authenticated:
        context = {}
        try:
            blog_obj = BlogModel.objects.get(slug=slug)
            if request.user != blog_obj.user:
                return redirect(home)
            b = blog_obj.content
            initial_dict = {'content': b}
            form = BlogForm(initial=initial_dict)

            if request.method == 'POST':
                form = BlogForm(request.POST)
                title = request.POST['title']
                user = request.user

                if form.is_valid():
                    content = form.cleaned_data['content']

                blog = BlogModel.objects.get(slug=slug)
                blog.user = user
                blog.title = title
                blog.content = content

                if request.FILES.get('image'):
                    blog.image = request.FILES['image']
                blog.save()

                messages.success(request, 'Your Blog upadated successfully!')
                return redirect(seeBlogs)

            context['blog_obj'] = blog_obj
            context['form'] = form
        except Exception as e:
            print(e)
        return render(request, 'blog/update_blog.html', context)
    else:
        messages.error(request, "Please Login!")
        return redirect(home)


def deleteBlog(request, slug):
    if request.user.is_authenticated:
        try:
            blog = BlogModel.objects.get(slug=slug)
            if request.user == blog.user:
                blog.delete()
                messages.success(request, 'Blog deleted successfully!')
                return redirect(seeBlogs)
            else:
                return redirect(home)
        except Exception as e:
            print(e)
    else:
        messages.error(request, "Please Login!")
        return redirect(home)


def search(request):
    context = {}
    try:
        query = request.GET['query']
        if len(query) > 78:
            search_blogs = BlogModel.objects.none()
            context['search_blogs'] = search_blogs
            messages.error(
                request, "You query length has exceeds , Please try less length of query")
        elif len(query) == 0:
            search_blogs = BlogModel.objects.none()
            context['search_blogs'] = search_blogs
            messages.warning(
                request, "You didn't pass any query. Please enter your query")
        else:
            searchBlogsTitle = BlogModel.objects.filter(title__icontains=query)
            searchBlogsContent = BlogModel.objects.filter(
                content__icontains=query)
            search_blogs = searchBlogsTitle.union(searchBlogsContent)
            if search_blogs.count() == 0:
                messages.warning(
                    request, 'No search results found. Please refine your query')
            else:
                p = Paginator(search_blogs, 3)
                pages = p.page_range
                pageNumber = request.GET.get('page')
                finalsearchpages = p.get_page(pageNumber)
                context['search_blogs'] = finalsearchpages

        context['query'] = query
        context['pages'] = pages
    except Exception as e:
        print(e)

    return render(request, 'blog/search.html', context)

# Comment Model Views

def commentAdd(request,slug):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                user_obj=User.objects.get(username=request.user.username)
                profile_obj=Profile.objects.get(user=request.user)                
                blog_obj=BlogModel.objects.get(slug=slug)
                comment=request.POST['comment']
                if len(comment) == 0:
                    messages.error(request,'Please write comment!')
                    return redirect(blogDetail,slug)
                CommentModel.objects.create(user=user_obj,profile=profile_obj,blog=blog_obj,comment=comment)
                print('create issue')
                messages.success(request,'Comment addd!')
                return redirect(blogDetail)
            else:
                messages.error(request,'something went wrong !')
                return redirect(home)
                
        else:
            messages.error(request,'Please login ! for comment')
    except Exception as e:
        print(e)
    return redirect(blogDetail,slug)

def commentUpdate(request):
    pass

def commentDelete(request,id):
    try:
        comment_obj=CommentModel.objects.get(id=id)
        if request.user.is_authenticated:
            if comment_obj.user==request.user:
                print('comment get')
                comment_obj.delete()
                messages.success(request, 'Comment deleted successfully!')
                return redirect(blogDetail,comment_obj.blog.slug)
            else:
                messages.error(request,"Sorry! You don't have permission to delete this comment")
        else:
            messages.error(request,'Please login!')
    except Exception as e:
        print(e)
    return redirect(blogDetail,comment_obj.blog.slug)



# Like Model Views

def likePost(request,slug):
    try:
        print("inside try")
        if request.user.is_authenticated:
            post=get_object_or_404(BlogModel, id=request.POST['post_id'])
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
            else:    
                post.likes.add(request.user)
            
            print(post)
            
        else:
            messages.error(request,'Please Login to like the post!')
    except Exception as e:
        print(e)
    return HttpResponseRedirect(reverse('blog_detail',args=[str(slug)]))

def follow(request):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                profile_obj=get_object_or_404(Profile,id=request.POST['follower'])
                if profile_obj.follower.filter(id=request.user.id).exists():
                    profile_obj.follower.remove(request.user)
                    messages.success(request,'You have unfollowed '+str(profile_obj.user.username))
                else:
                    profile_obj.follower.add(request.user)
                    messages.success(request,'You have followed '+str(profile_obj.user.username))
                return HttpResponseRedirect(reverse('blog_publisher',args=[str(profile_obj.user.username)]))
        else:
            messages.error(request,'Please login!')
    except Exception as e:
        print(e)
    return redirect(home)    