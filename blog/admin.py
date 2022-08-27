from django.contrib import admin

from blog.models import UserProfileInfo, User, Post
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Post)