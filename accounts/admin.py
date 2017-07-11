from django.contrib import admin
from .models import UserProfile, UserMessages
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    # form = TweetModelForm
    list_display = ["id", "first_name", 'last_name', 'user', 'timestamp']
    list_filter = ['id']
    class Meta:
        model = UserProfile


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserMessages)