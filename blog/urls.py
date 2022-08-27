from django.urls import re_path

from blog import views

# SET THE NAMESPACE!
app_name = 'blog'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    re_path(r'^register/',views.register,name='register'),
    re_path(r'^user_login/',views.user_login,name='user_login'),
    re_path(r'^profile/', views.myProfile, name="profile"),
    re_path(r'^create_blog/', views.create_blog, name="create_blog"),
    re_path(r'^blogs/', views.blog_list, name="blogs"),
    re_path(r'^blog_details/(?P<id>\d+)/$', views.blog_details, name="blog_details"),
    re_path(r'delete/(?P<id>\d+)/$',views.delete_post,name='delete'),
    re_path(r'^my_blogs/', views.my_blog_list, name="my_blogs"),
    re_path(r'^edit_profile/', views.edit_profile, name="edit_profile"),
   
    re_path(r'^user_blogs/(?P<id>\d+)/$', views.user_blogs, name="user_blogs"),

]