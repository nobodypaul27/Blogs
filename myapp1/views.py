from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Blog
# Create your views here.
def index(request):
    blogs = Blog.objects.all()
    return render(request, 'home.html',{'blogs':blogs})

def about(request):
    return render(request, 'about.html')

def user_register(request):
    if request.method == "POST":
        fname = request.POST.get('fisrtname')
        lname = request.POST.get('lastname')
        uname=request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1!=pass2:
            messages.warning(request,'password does not match')
            return redirect('user_register')
        elif User.objects.filter(username=uname).exists():
            messages.warning(request,'User name already exits')
            return redirect('user_register')
        elif User.objects.filter(email=email).exists():
            messages.warning(request,'Email  already exits')
            return redirect('user_register')
        else:  
            user = User.objects.create_user(first_name=fname,last_name=lname,username=uname,email=email,password=pass1)
            user.save()
            messages.success(request,'User has been registered successfully')
            return redirect('user_login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == "POST":
        username =  request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.warning(request,'Invalid Credincial')
            return redirect('user_register')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)        
    return redirect('index')


def post_blogs(request):
    if request.method == "POST":
        titl =  request.POST.get('Title')
        description = request.POST.get('Content')
        blog = Blog(title=titl,dsc=description,user_id=request.user)
        blog.save()
        messages.success(request,'blog post succesfully')
        return redirect('post_blogs')
    return render(request, 'blog_post.html')

def blog_details(request,id):
    blog = Blog.objects.get(id=id)
    return render(request,'blog_detail.html',{'blog':blog})