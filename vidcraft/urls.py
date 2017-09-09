"""vidcraft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from hashtags.views import HashTagView, HashTagList
from hashtags.api.views import TagVideoAPIView, TagListAPIView
from .views import home
from accounts.views import UserLoginFormView
from django.contrib.auth import views as auth_views
import notifications.urls
from django.contrib.auth import views as auth_views

#from vidcraft.core import views as core_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^about/', views.about, name='about'),
    url(r'^help/', views.help, name='help'),
    url(r'^policy/', views.policy, name='policy'),
    url(r'^hashtags/$', HashTagList.as_view(), name='hashtags'),
    url(r'^accounts/password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^accounts/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^accounts/reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^accounts/login/$', auth_views.login, name='authlogin'),
    url(r'^accounts/change_password/$', auth_views.password_change, {'post_change_redirect': 'accounts:home'}, name='password_change'),
    url(r'^notifications/api/unread_list/$', views.live_unread_notification_list, name='live_unread_list'),
    url('^notifications/', include(notifications.urls, namespace='notifications')),
    #url(r'^messages/', include('django_messages.urls')),

    url(r'^', include('charts.urls', namespace="charts")),
    url(r'^api/accounts/', include('accounts.api.urls', namespace='accountsapi')),
    url(r'^api/videos/', include('videos.api.urls', namespace='videosapi')),
    url(r'^api/charts/', include('charts.api.urls', namespace='chartsapi')),
    url(r'^', include('accounts.urls', namespace="accounts")),

    url(r'^', include('videos.urls', namespace="videos")),
    url(r'^api/hashtag/(?P<hashtag>.*)/$', TagVideoAPIView.as_view(), name='tag-tweet-api'),
    url(r'^api/hashtags/$', TagListAPIView.as_view(), name='tag-tweet-api'),
    url(r'^hashtag/(?P<hashtag>.*)/$', HashTagView.as_view(), name='hashtag'),

    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),
]

if settings.DEBUG:
    urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
