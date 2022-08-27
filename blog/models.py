from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.IntegerField(default=18)
    bio = models.CharField(max_length=150,default="nothing here, nothing here, nothing here, nothing here, nothing here")
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True, default='profile_pics/user.png')

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(User, default=1,null = True, on_delete=models.CASCADE)
   
    title = models.CharField(max_length=120)
    content = models.TextField(max_length=1000)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    blog_pic = models.ImageField(upload_to='blog_pics',blank=True, default='blog_pics/default.jpg')

    def __str__(self):
        return self.title