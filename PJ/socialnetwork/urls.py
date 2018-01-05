from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from socialnetwork import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add_post$', views.add_post, name='addpost'),
    url(r'^get_post$', views.get_post, name='getpost'),
    url(r'^add_comment$', views.add_comment, name='addcomment'),
    url(r'^profile/(?P<user>\w+)/$', views.profile, name='profile'),
    url(r'^login$', auth_views.login, {'template_name':'socialnetwork/login.html'}, name='login'),
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^edit_profile$', views.editProfile, name='edit_profile'),
    url(r'^photo/(?P<user>\w+)$', views.get_photo, name="photo"),
    url(r'^follow/(?P<user>\w+)$', views.follow, name='follow'),
    url(r'^unfollow/(?P<user>\w+)$', views.unfollow, name='unfollow'),
]