__author__ = 'OllyD'
from events.models import EventModel
from django.contrib.auth import get_user_model
from accounts.api.seralizers import UserProfileSerializer, UserSeralizer
from rest_framework import serializers
User = get_user_model()

class EventModelSerializer(serializers.ModelSerializer):
    attending_count = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    user = UserSeralizer()
    display_date = serializers.SerializerMethodField()
    is_attending = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    class Meta:
        model = EventModel
        fields = [
            'user',
            'id',
            'name',
            'street_address',
            'state',
            'city',
            'zipcode',
            'picture',
            'description',
            'date',
            'display_date',
            'start_time',
            'end_time',
            'address',
            'time',
            'attending',
            'attending_count',
            'is_attending',
            'url',

        ]

    def get_attending_count(self, obj):
        return obj.attending.all().count()

    def get_address(self, obj):
        return obj.street_address + ", " + obj.city + ", " + obj.state + " " + obj.zipcode

    def get_display_date(self, obj):
        return obj.date.strftime('%A. %B %d, %y')

    def get_time(self, obj):
        return str(obj.start_time.strftime('%I:%p')).replace("0", '') + " - " + str(obj.end_time.strftime('%I:%p')).replace("0", '')

    def get_is_attending(self, obj):
        request = self.context.get("request")
        user = request.user
        if user.is_authenticated():
            if request.user in obj.attending.all():
                return True
        return False

    def get_url(self, obj):
        return obj.get_absolute_url()




