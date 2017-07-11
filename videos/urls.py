__author__ = 'OllyD'
from django.conf.urls import url
from . import views

app_name = 'videos'


urlpatterns = [
            url(r'^videos/browse/$', views.VideoListView.as_view(), name="video_list"),
            url(r'^playlist/browse/$', views.PlaylistListView.as_view(), name="playlist_list"),
            url(r'^videos/category/(?P<category>[\w.@+-]+)/$', views.VideoCategoryListView.as_view(), name="video_category_list"),
            url(r'^videos/category/(?P<category>[\w.@+-]+)/(?P<genrename>[\w.@+-]+)/$', views.VideoGenreListView.as_view(), name="video_genre_list"),
            url(r'^video/(?P<pk>\d+)/$', views.VideoDetailView.as_view(), name="video_detail"),
            url(r'^playlist/(?P<pk>\d+)/$', views.PlaylistDetailView.as_view(), name="playlist_detail"),
            url(r'^video/(?P<pk>\d+)/update/$', views.VideoUpdateView.as_view(), name="video_update"),
            url(r'^videos/upload/$', views.VideoUploadView.as_view(), name="video_upload"),

        ]