__author__ = 'OllyD'

app_name = "accountsapi"
from django.conf.urls import url
from . import views
#(?P<username>[\w.@+-]+)

urlpatterns = [
    #url(r'^$', UserView.as_view(), name='list'),
    url(r'^register/$', views.UserCreateAPIView.as_view(), name='register'),
    url(r'^$', views.UserProfileListAPIView.as_view(), name='list'),
    url(r'^(?P<username>[\w.@+-]+)/videos/$', views.UserVideoAPIView.as_view(), name='user-videos'),
    url(r'^videos/following/$', views.FollowingVideosAPIView.as_view(), name='following-videos'),
    url(r'^(?P<username>[\w.@+-]+)/followers/$', views.UserFollowerAPIView.as_view(), name='user-followers'),
    url(r'^(?P<username>[\w.@+-]+)/following/$', views.UserFollowingAPIView.as_view(), name='user-following'),
    url(r'^(?P<username>[\w.@+-]+)/liked/$', views.UserLikedAPIView.as_view(), name='user-liked'),
    url(r'^(?P<username>[\w.@+-]+)/shared/$', views.UserSharedAPIView.as_view(), name='user-liked'),
    url(r'^(?P<username>[\w.@+-]+)/follow/$', views.UserFollowToggleAPIView.as_view(), name='follow-toggle'),
    url(r'^(?P<user__username>[\w.@+-]+)$', views.UserDetailAPIView.as_view(), name='user-detailAPI'),
    url(r'^(?P<pk>\d+)/update/$', views.UserUpdateAPIView.as_view(), name='user-updateAPI'),
    #url(r'^(?P<username>[\w.@+-]+)/$', UserDetailAPIView.as_view(), name='user-detailAPI'),
   # url(r'^(?P<pk>\d+)/like/$', FollowToggleAPIView.as_view(), name='follow-toggle'),
]