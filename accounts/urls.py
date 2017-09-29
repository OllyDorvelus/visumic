__author__ = 'OllyD'

from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [

    url(r'^login/$', views.UserLoginFormView.as_view(), name="login"),
    url(r'^register/$', views.UserRegisterFormView.as_view(), name="register"),
    url(r'^$', views.home, name="home"),
    url(r'^social/$', views.social, name="social"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^crafters/$', views.ProfileListView.as_view(), name='profile_list'),
    url(r'^manage/$', views.ProfileUpdateView.as_view(), name='profile_update'),
    url(r'^manage/account/$', views.UserUpdateView.as_view(), name='account_update'),
    url(r'^(?P<username>[\w.@+-]+)/$', views.UserDetailView.as_view(), name='profile_detail'),
    url(r'^(?P<username>[\w.@+-]+)/following/$', views.UserDetailFollowingView.as_view(), name='profile_detail-following'),
    url(r'^(?P<username>[\w.@+-]+)/followers$', views.UserDetailFollowerView.as_view(), name='profile_detail-followers'),
    url(r'^(?P<username>[\w.@+-]+)/liked/$', views.UserDetailLikedView.as_view(), name='profile_detail-liked'),
    url(r'^(?P<username>[\w.@+-]+)/shared/$', views.UserDetailSharedView.as_view(), name='profile_detail-shared'),
    url(r'^(?P<username>[\w.@+-]+)/playlist/$', views.UserDetailPlayListView.as_view(), name='profile_detail-playlist'),
    url(r'^(?P<username>[\w.@+-]+)/events/$', views.UserDetailEventView.as_view(), name='profile_detail-events'),

    #url(r'^(?P<pk>[0-9]+)/manage/$', views.ProfileUpdateView.as_view(), name='profile_update')



]