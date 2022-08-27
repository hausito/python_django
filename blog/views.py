from django.shortcuts import render, get_object_or_404
from blog.forms import UserForm, UserProfileInfoForm, BlogForm, EditUserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import UserProfileInfo, Post
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def index(request):
    return render(request,'blog/index.html')
@login_required
def special(request):
    return HttpResponse("You are logged in !")
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'blog/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username1 = request.POST.get('username')
        password1 = request.POST.get('password')

        user = authenticate(username = username1, password = password1)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username1,password1))
            return render(request, 'blog/login.html', {"text":"Invalid dates"})
    else:
        return render(request, 'blog/login.html', {})
def myProfile(request):
    #Userio = UserProfileInfo.objects.filter(user_id = User.id)
    #portfolio_link = Userio.get().porfolio_site
   
    #a = User.objects.filter(id = 1)
    #link = a.get().email
    connected_username = request.user.username
    connected_user = User.objects.filter(username = connected_username)
    current_id = connected_user.get().id
    username = connected_user.get().username
    connected_user_profile = UserProfileInfo.objects.filter(user_id = current_id)
    
    avatar = connected_user_profile.get().profile_pic
    age = connected_user_profile.get().age
    bio = connected_user_profile.get().bio

    first_name = connected_user.get().first_name
    last_name = connected_user.get().last_name
    full_name = first_name + " " + last_name
    email = connected_user.get().email

    
  
    

    return render(request, 'blog/profile.html', {"first_name": first_name,"avatar": avatar, "full_name": full_name, "email": email, "age": age, "bio": bio})

def create_blog(request):
    if request.method == 'POST':
       
        blog_form = BlogForm(data=request.POST)
        
        
        if blog_form.is_valid():
            obj = blog_form.save(commit = False)
            obj.user = request.user
          
            if 'blog_pic' in request.FILES:
                print('found it')
                obj.blog_pic = request.FILES['blog_pic']
            obj.save()
            blog_form = BlogForm()
            
          
            
           
            return HttpResponseRedirect(reverse('index'))

    else:
        blog_form = BlogForm()
       
    return render(request,'blog/create_blog.html',{'blog_form': blog_form})

def blog_list(request, key = None):
    

    
    #first_name = connected_user.get().first_name
    #last_name = connected_user.get().last_name
    #full_name = first_name + " " + last_name
    new_blogs = Post.objects.all()
   
    query = request.GET.get("q")
    if query:
        new_blogs = new_blogs.filter(title__icontains=query)
    else:
        query = key
    #user_username = User.filter(id = blog.user_id).get().username
    
    #contact_list = Contacts.objects.all()
    paginator = Paginator(new_blogs, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    blog_list= paginator.get_page(page)
  
    


    return render(request, 'blog/blogs.html', {'blog_list': blog_list, "key":True})

def blog_details(request, id=None):
    instance = get_object_or_404(Post, id=id)
    
    connected_user = User.objects.filter(id = instance.user_id)
    user_id = connected_user.get().id
    connected_profile = UserProfileInfo.objects.filter(user_id = user_id)
    avatar = connected_profile.get().profile_pic
    age = connected_profile.get().age
    bio = connected_profile.get().bio

    return render(request, 'blog/blog_details.html', {"avatar": avatar,"instance":instance,"age": age, "bio": bio})
def delete_post(request,id=None):
    post_to_delete=Post.objects.get(id=id)
    post_to_delete.delete()
    return HttpResponseRedirect(reverse('index'))

def my_blog_list(request):
    

    
    #first_name = connected_user.get().first_name
    #last_name = connected_user.get().last_name
    #full_name = first_name + " " + last_name

   
    
    new_blogs = Post.objects.all()
    

    connected_username = request.user.username
    connected_user = User.objects.filter(username = connected_username)
    current_id = connected_user.get().id
    query = request.GET.get("q")
    if query:
        new_blogs_1 = new_blogs.filter(title__icontains=query)
        new_blogs_2 = new_blogs_1.filter(user_id = current_id)
    else:
        new_blogs_2 = Post.objects.filter(user_id = current_id)
    

    paginator = Paginator(new_blogs_2, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    blog_list = paginator.get_page(page)
  
    


    return render(request, 'blog/blogs.html', {'blog_list': blog_list, "key":False})


def edit_profile(request):
   

    if request.method == 'POST':
        form_1 = EditUserForm(data = request.POST, instance=request.user)
        fm = UserProfileInfoForm(data=request.POST)
        
        connected_username = request.user.username
        connected_user = User.objects.filter(username = connected_username)
        user_id = connected_user.get().id
        connected_profile = UserProfileInfo.objects.filter(user_id = user_id)
        profile_id = connected_profile.get().id
        print(profile_id)

        if form_1.is_valid() and fm.is_valid():
            form_1.save()
            fm.save(commit = False)
            if 'profile_pic' in request.FILES:
                print('found it')
                profile_pic = request.FILES['profile_pic']
                pw = profile_pic
            else:
                pw = connected_profile.get().profile_pic
                print("not found")
            nm = fm.cleaned_data['age']
            
            em = fm.cleaned_data['bio']
            if em :
                ee = em
            else:
                ee = connected_profile.get().bio
            reg = UserProfileInfo(id=profile_id,age=nm, bio=ee, profile_pic=pw, user_id = user_id)
            reg.save()
            connected_username = request.user.username
            connected_user = User.objects.filter(username = connected_username)
            current_id = connected_user.get().id
            username = connected_user.get().username
            connected_user_profile = UserProfileInfo.objects.filter(user_id = current_id)
    
            avatar = connected_user_profile.get().profile_pic
            age = connected_user_profile.get().age
            bio = connected_user_profile.get().bio

            first_name = connected_user.get().first_name
            last_name = connected_user.get().last_name
            full_name = first_name + " " + last_name
            email = connected_user.get().email
            return render(request, 'blog/profile.html', {"first_name": first_name,"avatar": avatar, "full_name": full_name, "email": email, "age": age, "bio": bio})

    else:
        form_1 = EditUserForm(instance=request.user)
        fm = UserProfileInfoForm()
        args = {'form_1':form_1, 'form_2':fm}
    return render(request, 'blog/edit_profile.html', args)

def user_blogs(request, id = None):
    
    new_blogs = Post.objects.all()
    

    query = request.GET.get("q")
    if query:
        new_blogs_1 = new_blogs.filter(title__icontains=query)
        new_blogs_2 = new_blogs_1.filter(id = id)
    else:
        new_blogs_2 = Post.objects.filter(user_id = id)
    

    paginator = Paginator(new_blogs_2, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    blog_list = paginator.get_page(page)
  
    


    return render(request, 'blog/blogs.html', {'blog_list': blog_list, "key":False})

