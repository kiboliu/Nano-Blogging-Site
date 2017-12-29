from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from socialnetwork import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^add_post$', views.add_post),
    url(r'^profile/(?P<user>\w+)/$', views.profile),
    url(r'^login$', auth_views.login, {'template_name':'socialnetwork/login.html'}, name='login'),
    url(r'^logout$', auth_views.logout_then_login),
    url(r'^register$', views.register),
]