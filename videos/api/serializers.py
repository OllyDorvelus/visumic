__author__ = 'OllyD'
from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from rest_framework import serializers
from videos.models import VideoModel, CommentModel, ShareModel, ShareCommentModel, GenreModel, PlaylistModel
#from accounts.api.seralizers import UserDisplaySerializer
from django.utils.timesince import timesince
from accounts.api.seralizers import UserProfileSerializer
from django.urls import reverse_lazy
from datetime import datetime, timedelta

User = get_user_model()

# class UserProfileDisplaySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = [
#             'user_img',
#             'bio',
#         ]

class UserDisplaySerializer(serializers.ModelSerializer):
    # follower_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    video_count = serializers.SerializerMethodField()
    profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'url',
            'video_count',
            'profile',

            ]

    def get_url(self, obj):
        return reverse_lazy("accounts:profile_detail", kwargs={"username": obj.username})

    def get_video_count(self, obj):
        return obj.videos.count()


class VideoModelSerializer(serializers.ModelSerializer):
   # url = serializers.SerializerMethodField()
    user = UserDisplaySerializer(read_only=True)
    url = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()
    shares_count = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    date_display = serializers.SerializerMethodField()
    daily_views = serializers.SerializerMethodField()
    comments = serializers.StringRelatedField(many=True, read_only=True)
   # genre = serializers.StringRelatedField()
    class Meta:
        model = VideoModel
        fields = [
            'id',
            'user',
            'video',
            'title',
            'liked',
            'likes_count',
            'did_like',
            'description',
            'thumbnail',
            'genre',
            'url',
            'comments',
            'playlistvideos',
            'shares_count',
            'views',
            'daily_views',
            'date_display',
            'timesince',
            'timestamp',
            ]
        read_only_fields = [
           'id',
           'video',
           'comments',
           'date_display',
           'liked',
           #'views',

          # 'thumbnail',

       ]


    def get_url(self, obj):
        return reverse_lazy("videos:video_detail", kwargs={"pk": obj.pk})

    def get_likes_count(self, obj):
        return obj.liked.count()
        return

    def get_shares_count(self, obj):
        return obj.shares.count()

    def get_did_like(self, obj):
        request = self.context.get("request")
        user = request.user
        if user.is_authenticated():
            if user in obj.liked.all():
                return True
        return False

    def get_views(self, obj):
        return obj.hit_count.hits
        return obj.hit_count.hits_in_last(days=1)

    def get_daily_views(self, obj):
        #return obj.hit_count.hits
        return obj.hit_count.hits_in_last(days=1)

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"

    def get_date_display(self, obj):
       # return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")
        return obj.timestamp.strftime("%m-%d-%Y")

class GenreModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreModel
        fields = [
            'genrename',
            'parent'
        ]

class VideoModelEditSerializer(serializers.ModelSerializer):
   # url = serializers.SerializerMethodField()
    user = UserDisplaySerializer(read_only=True)
    class Meta:
        model = VideoModel
        fields = [
            'user',
            'title',
            'description',
            'genre'


        ]
class ParentCommentModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True) #write_only
    did_like = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = CommentModel
        fields = [
            'id',
            'video',
            'comment',
            'timestamp',
            'user',
            'likedcmt',
            'likes_count',
            'did_like',
            'parent',
            'reply',
            'replies',

        ]
        read_only_fields = [

        ]

    def get_did_like(self, obj):
        request = self.context.get("request")
        user = request.user
        if user.is_authenticated():
            if user in obj.likedcmt.all():
                return True
        return False


    def get_likes_count(self, obj):
        return obj.likedcmt.count()


class CommentModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)
    video = VideoModelSerializer(read_only=True)
    did_like = serializers.SerializerMethodField()
    likedcmt = serializers.StringRelatedField(many=True)
    parent = ParentCommentModelSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    class Meta:
        model = CommentModel
        fields = [
            'id',
            'video',
            'comment',
            'timestamp',
            'user',
            'likedcmt',
            'likes_count',
            'did_like',
            'parent',
            'timesince',
            'reply',
            'replies',
        ]
        read_only_fields = [
            'reply',
            'replies',
        ]

    def get_did_like(self, obj):
        request = self.context.get("request")
        user = request.user
        if user.is_authenticated():
            if user in obj.likedcmt.all():
                return True
        return False

    def get_likes_count(self, obj):
        return obj.likedcmt.count()

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"

class ShareModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)
    video = VideoModelSerializer(read_only=True)
    timesince = serializers.SerializerMethodField()
    #sharecomments = ShareModelCommentSerializer(read_only=True)
    class Meta:
        model = ShareModel
        fields = [
            'id',
            'video',
            'content',
            'sharecomments',
            'timestamp',
            'timesince',
            'user',
        ]

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"


class ShareModelCommentSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)
    share = ShareModelSerializer(read_only=True)

    class Meta:
        model = ShareCommentModel
        fields = [
            'id',
            'user',
            'comment',
            'share',
            'timestamp',
        ]



class PlaylistModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)
    url = serializers.SerializerMethodField()
    video_count = serializers.SerializerMethodField()
    is_empty = serializers.SerializerMethodField()
    videos = VideoModelSerializer(many=True, read_only=True)
    #videos = serializers.StringRelatedField(many=True, read_only=True)
    #videos = serializers.HyperlinkedIdentityField(view_name='url')
   # playlist_img = serializers.SerializerMethodField()
    class Meta:
        model = PlaylistModel
        fields = [
            'user',
            'id',
            'name',
            'description',
            'is_empty',
             #'playlist_img',
            'url',
            'video_count',
            'videos',
        ]
    def get_url(self, obj):
        return reverse_lazy("videos:playlist_detail", kwargs={"pk": obj.pk})

    def get_video_count(self, obj):
        return obj.videos.all().count()

    def get_is_empty(self, obj):
        if obj.videos.all().count() == 0:
            return True
        return False

    # def get_playlist_img(self, obj):
    #     return VideoModelSerializer()








