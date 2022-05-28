from django.http import HttpResponse
from django.shortcuts import redirect, render
from .form import *
from django.contrib import messages
from django.contrib.auth import logout
from django.core.paginator import Paginator


def home(request):
    try:
        blogs = BlogModel.objects.all()
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
    if request.user.is_authenticated:
        messages.error(request, "You already Logged in!")
        return redirect(home)
    else:
        return render(request, 'blog/login.html')

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
        messages.error(request,'something went wrong')
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
                    profile_obj.avatar= request.FILES['avatar']

                if len(bio)>150:
                    messages.error(request,"Bio lenght can not be more than 150 characters")
                    raise Exception('Bio lenght can not be more than 150 characters')

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
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e)
    return render(request, 'blog/blog_detail.html', context)

def blogPublisher(request,username):
    try:
        user_obj=User.objects.get(username=username)
        if request.user.username==username:
            return redirect(profile)
        blogs= BlogModel.objects.filter(user=user_obj)
        profile_obj=Profile.objects.get(user=user_obj)
        context={'profile':profile_obj,'blogs':blogs}
    except Exception as e:
        print(e)

    return render(request,'blog/public_profile.html',context)

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

