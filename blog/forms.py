from django import forms
from blog.models import UserProfileInfo, Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    class Meta():
        model = User
        fields = ('username','password','first_name','last_name','email')
        help_texts = {
            'username': None,
        }
class UserProfileInfoForm(forms.ModelForm):
    
    bio = forms.CharField(min_length=50, required=False)
    class Meta():
        model = UserProfileInfo
        fields = ('age','bio','profile_pic')
   
class BlogForm(forms.ModelForm):
    content = forms.CharField(required=True, min_length=400)
    
    class Meta():
        model = Post
        fields = ('title','content','blog_pic')

class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
        )
