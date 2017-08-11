from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from rest_framework import serializers
#from videos.api.serializers import VideoModelSerializer
from videos.models import VideoModel
from hashtags.models import HashTagModel
from django.urls import reverse_lazy
#from django.utils.timesince import ti


class HashtagModelSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = HashTagModel
        fields = [
            'tag',
            'timestamp',
            'url'
        ]

    def get_url(self, obj):
        return reverse_lazy("hashtag", kwargs={"hashtag": obj.tag})