from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .form import *
from django.contrib import messages
from django.contrib.auth import logout,login,authenticate
from django.core.paginator import Paginator
from django.urls import reverse_lazy,reverse
from django.contrib.sites.shortcuts import get_current_site
from .helpers import *
from django.db.models import Max, Count


def home(request):
    context={}
    try:
        blogs = BlogModel.objects.all().order_by('-id')
        try:
            allblogs=BlogModel.objects.annotate(Count('likes'))
            maxlist=[]        
            for blog in allblogs:
                maxlist.append(blog.likes__count)

            for blog in allblogs:
                if max(maxlist) == blog.likes__count:
                    featured=blog
                    break
            featured_blog=featured
        except:
            pass
        paginator = Paginator(blogs, 3)
        pages = paginator.page_range
        pageNumber = request.GET.get('page')
        finalBlogpage = paginator.get_page(pageNumber)
        context = {'blogs': finalBlogpage, 'pages': pages, 'featured_blog':featured_blog}
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            verify = profile.is_varified
            if not verify:
                messages.warning(request, 'Please verify your Account!')
            if not profile.is_email_varified:
                messages.warning(request,'Please Verify your Email')
    except Exception as e:
        print('Printing Home Exception')
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
                    profile_obj=Profile.objects.get(user=user_obj)
                    if profile_obj.is_varified:
                        messages.success(request,'You are logged in successfully!')
                    return redirect(home)
                else:
                    messages.error(request,'Please enter a right credentials!')
    except Exception as e:
        print('Printing signin Exception')
        print(e)
    return render(request, 'blog/signin.html')

def checkUsername(request):
    user_obj=User.objects.filter(username=request.GET['username'])
    if user_obj:
        return HttpResponse('false')
    else:
        return HttpResponse('true')

def register(request):
    try:
        if request.user.is_authenticated:
            messages.error(request, "Please logout then you can Signup!")
            return redirect(home)
        else:
            if request.method == "POST":
                username=request.POST['username']
                fname=request.POST['fname']
                lname=request.POST['lname']
                email=request.POST['email']
                password=request.POST['password']
                if username == '':
                    messages.error(request,'Username is must!')
                    return redirect(register)
                elif fname == '':
                    messages.error(request,'First is must!')
                    return redirect(register)
                elif lname == '':
                    messages.error(request,'Last name is must!')
                    return redirect(register)
                elif email == '':
                    messages.error(request,'Email is must!')
                    return redirect(register)
                elif password == '':
                    messages.error(request,'password is must!')
                    return redirect(register)
                else:
                    user_obj=User.objects.create(username=username)
                    user_obj.set_password(password)
                    user_obj.first_name=fname
                    user_obj.last_name=lname
                    user_obj.email=email
                    user_obj.save()

                    token=generate_random_string(20)
                    Profile.objects.create(user=user_obj,token=token)
                    domain_name='https://sunil-code-blog.herokuapp.com/'
                    send_mail_to_user(token,email,domain_name)
                    messages.success(request,'User Created sucessfully! Please check your email in order to activate your account')
                    return redirect(home)
    except Exception as e:
        print('Printing Register Exception')
        print(e)

    return render(request, 'blog/register.html')


def verify(request, token):
    try:
        profile_obj = Profile.objects.filter(token=token).first()

        if profile_obj:
            profile_obj.is_varified = True
            profile_obj.save()
            messages.success(request,'Your account has been activated successfully! Please login.')
        return redirect(signin)
    except Exception as e:
        print('Printing verify Exception')
        print(e)

def emailVerify(request,token):
    try:
        print('inside try block')
        profile_obj = Profile.objects.filter(token=token).first()
        
        if profile_obj:
            profile_obj.is_email_varified= True
            profile_obj.save()
            messages.success(request,"Your email verification has been completed successfully!")
        else:
            messages.error(request,'Something went wrong.')
    except Exception as e:
        print('Printing EmailVerify Exception')
        print(e)
    return redirect(home)
        
def forgetPassword(request):
    try:
        if request.method == 'POST':
            email=request.POST['email']
            user_obj=User.objects.get(email=email)
            if not user_obj:
                messages.error(request,'Please Enter Your verified Email')
                return redirect(forgetPassword)
            token=generate_random_string(20)
            profile_obj=Profile.objects.get(user=user_obj)
            profile_obj.token=token
            profile_obj.save()
            domain_name='https://sunil-code-blog.herokuapp.com/'
            status=send_forget_email(token,email,domain_name)
            if status =='success':
                messages.success(request,'We have sent you email. Please check that out! ')
            
            return redirect(forgetPassword)
    except Exception as e:
        print('Printing forget password Exception')
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
        else:
            return HttpResponse('''<h2>Your forget password request has been expired. Please Request Again.</h2> <a href="/forget-password">For New Request Click here</a>''')
            
    except Exception as e:
        print('Printing Set New Password Exception')
        print(e)
    return HttpResponse("<h2>Bade request 404</h2>")

def saveForgetPassword(request):
    try:
        if request.method == 'POST':
            username=request.POST['username']
            new_password=request.POST['new_password']
            confirm_password=request.POST['confirom_password']
            user_obj=User.objects.get(username=username)
            profile_obj=Profile.objects.get(user=user_obj)
            if confirm_password == new_password:
                user_obj.set_password(confirm_password)
                user_obj.save()
                token=generate_random_string(20)
                profile_obj.token=token
                profile_obj.save()

                messages.success(request,'Your Password has been changed succfully!')
                return redirect(signin)
            else:
                messages.error(request,'Please enter Both same password')
    except Exception as e:
        print('Printing Save New Password Exception')
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
        print('Printing Profile Exception')
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
                    if not user.email == email :
                        token=generate_random_string(20)
                        profile_obj.token=token
                        profile_obj.save()
                        domain_name='https://sunil-code-blog.herokuapp.com/'
                        print(domain_name)
                        
                        status=sendMailForEmailVerification(token,email,domain_name)
                        if status == 'success':
                            messages.success(request,"Please Check your Email to verify eamil")
                            user.email=email
                            profile_obj.is_email_varified=False

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
        print('Printing Update Exception')
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
            print('Printing Add blog Exception')
            print(e)
        return render(request, 'blog/add_blog.html', context)
    else:
        messages.error(request, "Please Login!")
        return redirect(home)


def blogDetail(request, slug):
    context = {}
    try:
        # blog_obj = BlogModel.objects.filter(slug=slug).first()
        blog_obj=BlogModel.objects.get(slug=slug)
        
        comments_obj=CommentModel.objects.filter(blog=blog_obj)
        liked=False
        if blog_obj.likes.filter(id=request.user.id):
            liked=True
        else:
            liked=False
        context={'blog_obj':blog_obj}
        context['comments_obj'] = comments_obj
        context['liked'] = liked
    except Exception as e:
        print('Printing Blog Details Exception')
        print(e)
    return render(request, 'blog/blog_detail.html', context)


def blogPublisher(request, username):
    context={}
    try:
        if request.user.username == username:
            return redirect(profile)
        else:
            user_obj=User.objects.get(username=username)
            blogs = BlogModel.objects.filter(user=user_obj)
            profile_obj = Profile.objects.get(user=user_obj)
            followed=False
            follow_obj=profile_obj.follower.filter(id=request.user.id).first()
            if follow_obj:
                followed=True
            else:
                followed=False
            context = {'profile': profile_obj, 'blogs': blogs,'followed':followed}
        
    except Exception as e:
        print('Printing Blog Pusblisher Exception')
        print(e)

    return render(request, 'blog/public_profile.html', context)


def seeBlogs(request):
    try:
        context = {}
        if request.user.is_authenticated:
            blog_objs = BlogModel.objects.filter(user=request.user).order_by('-id')
            context['blog_objs'] = blog_objs
            return render(request, 'blog/see_blogs.html', context)
        else:
            messages.error(request, "Please Login!")
            return redirect(home)
    except Exception as e:
        print('Printing See blogs Exception')
        print(e)


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
                context['search_blogs'] = search_blogs

        context['query'] = query
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
        print('printing like post exction')
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