__author__ = 'OllyD'
app_name = "videosapi"
from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', UserView.as_view(), name='list'),
    url(r'^$', views.VideoModelListAPIView.as_view(), name='videoapilist'),
    url(r'^random/$', views.RandomVideoAPIView.as_view(), name='randomvideo'),
    url(r'^recent/$', views.VideoModelRecentAPIView.as_view(), name='videoapilistrecent'),
    url(r'^genre/(?P<genrename>[\w.@+-]+)/$', views.VideoGenreAPIView.as_view(), name='videoapigenrelist'),
    url(r'^category/(?P<category>[\w.@+-]+)/(?P<genrename>[\w.@+-]+)/$', views.VideoNewGenreAPIView.as_view(), name='videoapigenreelist'), #put an extra e
    url(r'^category/(?P<genrename>[\w.@+-]+)/$', views.VideoCategoryAPIView.as_view(), name='videoapicategorylist'),
    # url(r'^comments/$', CommentModelListAPIView.as_view(), name='commentapilist'),
    url(r'^(?P<pk>\d+)/like/$', views.VideoLikeToggleAPIView.as_view(), name='like-video-toggle'),
    url(r'^comment/(?P<pk>\d+)/like/$', views.CommentLikeToggleAPIView.as_view(), name='like-comment-toggle'),
    url(r'^(?P<video>\d+)/comments/$', views.CommentModelListAPIView.as_view(), name='commentapilist'),
    url(r'^comment/(?P<pk>\d+)/replies/$', views.CommentModelReplyListAPIView.as_view(), name='commentreplyapilist'),
    url(r'^share/(?P<share>\d+)/share-comments/$', views.ShareCommentModelListAPIView.as_view(), name='sharecommentapilist'),
    url(r'^share/(?P<pk>\d+)/$', views.ShareDetailAPIView.as_view(), name='shareapidetail'),
    url(r'^(?P<video>\d+)/related/$', views.RelatedListAPIView.as_view(), name='relatedvideolist'),
    url(r'^(?P<video>\d+)/shares/$', views.ShareListAPIView.as_view(), name='shareapilist'),
    url(r'^(?P<video>\d+)/shares/create/$', views.ShareCreateAPIView.as_view(), name='shareapicreate'),
    url(r'^(?P<video>\d+)/comments/create/$', views.CommentCreateAPIView.as_view(), name='commentapicreate'),
    url(r'^comment/(?P<pk>\d+)/reply/create/$', views.ReplyCommentCreateAPIView.as_view(), name='commentreplyapicreate'),
    url(r'^(?P<pk>\d+)/$', views.VideoModelDetailAPIView.as_view(), name='videoapidetail'),
    url(r'^comment/(?P<pk>\d+)/$', views.CommentModelDetailAPIView.as_view(), name='commentapidetail'),
    url(r'^(?P<pk>\d+)/update/$', views.VideoModelUpdateAPIView.as_view(), name='videoapiupdate'),
    url(r'^(?P<pk>\d+)/delete/$', views.VideoModelDeleteAPIView.as_view(), name='videoapidelete'),
    url(r'^shares/following/$', views.ShareFollowingAPIView.as_view(), name='following-share-videos'),
    url(r'^playlist/$', views.PlaylistListAPIView.as_view(), name='playlist-list'),
    url(r'^playlist/(?P<pk>\d+)/$', views.PlaylistDetailAPIView.as_view(), name='playlist-detail'),
    url(r'^(?P<username>[\w.@+-]+)/playlist/$', views.UserPlaylistAPIView.as_view(), name='user-playlist'),
    url(r'^playlist/(?P<pk>\d+)/videos/$', views.PlaylistVideosAPIView.as_view(), name='playlist-videos'),
    url(r'^playlist/create/$', views.PlaylistCreateAPIView.as_view(), name='create-playlist'),
    url(r'^playlist/(?P<pk>\d+)/add/(?P<id>\d+)/$', views.AddVideoToPlaylistAPIView.as_view(), name='add-playlist'),
    url(r'^playlist/(?P<pk>\d+)/remove/(?P<id>\d+)/$', views.RemoveVideoToPlaylistAPIView.as_view(), name='remove-playlist'),

    #url(r'^(?P<username>[\w.@+-]+)/$', UserDetailAPIView.as_view(), name='user-detailAPI'),
   # url(r'^(?P<pk>\d+)/like/$', FollowToggleAPIView.as_view(), name='follow-toggle'),
]