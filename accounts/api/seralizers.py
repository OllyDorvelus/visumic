__author__ = 'OllyD'

from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from rest_framework import serializers
#from videos.api.serializers import VideoModelSerializer
from videos.models import VideoModel
from django.utils.timesince import timesince
from django.urls import reverse_lazy
from django.db.models import Count, Avg, Max, Min
from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )

User = get_user_model()
class VideoModelSerializer(serializers.ModelSerializer):
   # url = serializers.SerializerMethodField()

    class Meta:
        model = VideoModel
        fields = [
            'id',
            'video',
            'title',
            #'liked',
            'description',
        ]

class UserDisplaySerializer(serializers.ModelSerializer):
    # follower_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    video_count = serializers.SerializerMethodField()
    videos = serializers.StringRelatedField(many=True)
    shared = serializers.StringRelatedField(many=True)
    liked = serializers.StringRelatedField(many=True)
    shared_count = serializers.SerializerMethodField()
    all_likes = serializers.SerializerMethodField()
    all_views = serializers.SerializerMethodField()
    all_shares = serializers.SerializerMethodField()
    all_comments = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'url',
            'videos',
            'video_count',
            'liked',
            'shared',
            'shared_count',
            'author',
            'all_likes',
            'all_views',
            'all_shares',
            'all_comments',
            ]

    def get_url(self, obj):
        return reverse_lazy("accounts:profile_detail", kwargs={"username": obj.username})

    def get_video_count(self, obj):
        return obj.videos.count()

    def get_all_likes(self, obj):
        #all_likes = VideoModel.objects.filter(user=obj).annotate(num_likes = Count('liked')).count()
        all_likes = VideoModel.objects.filter(user=obj).aggregate(Count('liked'))
        return all_likes

    def get_all_views(self, obj):
        all_views = VideoModel.objects.filter(user=obj).aggregate(Count('views__hit'))
        #all_views = VideoModel.objects.filter(user=obj).annotate(Count('views')).count()
       # all_views = VideoModel.objects.get(pk=10).hit_count.hits
        return all_views

    def get_all_shares(self, obj):
        all_shares = VideoModel.objects.filter(user=obj).aggregate(Count('shares'))
        return all_shares

    def get_all_comments(self, obj):
        all_comments = User.objects.get(pk=obj.pk).author.count()
        return all_comments


       # videos = VideoModel.objects.filter(user=obj)
       # return videos.liked.count()

    def get_shared_count(self, obj):
        return obj.shared.all().count()

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)

    is_following = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    following = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username')

    #date_display = serializers.SerializerMethodField()
    # timesince = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'following',
            'user_img',
            'first_name',
            'last_name',
            'bio',
            'profile_banner',
            'timestamp',
            'is_following',
            'follower_count',
            'following_count',






        ]

    # def get_date_display(self, obj):
    #      return obj.joindate.strftime("%b %d, %Y at %I:%M %p")
    #
    # def get_timesince(self, obj):
    #     return timesince(obj.timestamp) + " ago"
    def get_is_following(self, obj):
        request = self.context.get("request")
        user = request.user
        if user.is_authenticated():
            if obj.user in user.profile.following.all():
                return True
        return False

    def get_follower_count(self, obj):
        return obj.user.followed_by.all().count()

    def get_following_count(self, obj):
        return obj.following.all().count()




# class UserFollowingSeralizer(serializers.ModelSerializer):
#     user = UserDisplaySerializer(read_only=True)
#     profile = UserProfileSerializer(read_only=True)
#     class Meta:
#         model = UserProfile

class UserSeralizer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    video_count = serializers.SerializerMethodField()
    videos = serializers.StringRelatedField(many=True)
    profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'url',
            'videos',
            'video_count',
            'profile',
        ]

    def get_url(self, obj):
        return reverse_lazy("accounts:profile_detail", kwargs={"username": obj.username})

    def get_video_count(self, obj):
        return obj.videos.count()


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
    email2 = EmailField(label='Confirm Email')
    password2 = CharField(label='Confirm Password', write_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
           'password2',

        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }

       # extra_kwargs = {'password2': {'write_only': True}}

        # write_only_fields = [
        #     'password',
        #     'password2'
        # ]

    def validate(self, data):
        # email = data['email']
        # user_qs = User.objects.filter(email=email)
        # if user_qs.exists():
        #     raise ValidationError("This user has already registered.")
        return data


    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")

        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")

        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")
        return value

    def validate_password2(self, value):
        data = self.get_initial()
        password1 = data.get("password")
        password2 = value
        if password1 != password2:
            raise ValidationError("Passwords must match.")
        return value

    def validate_username(self, value):
        username = value
       # username = self.cleaned_data.get('username')
        if User.objects.filter(username__icontains=username).exists():
            raise ValidationError("This username is taken")
        return username



    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
                username = username,
                email = email
            )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField()
    email = EmailField(label='Email Address')
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',

        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }
    def validate(self, data):
        # email = data['email']
        # user_qs = User.objects.filter(email=email)
        # if user_qs.exists():
        #     raise ValidationError("This user has already registered.")
        return data
