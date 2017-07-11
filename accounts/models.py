from django.db import models

from .validators import validate_file_extension
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import post_save, post_delete
from celery import Celery

app = Celery('hello', broker='amqp://guest@localhost//')

@app.task
def hello():
    return 'hello world'
# Create your models here.



class UserProfileManager(models.Manager):
    use_for_related_fields = True
    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def follow_toggle(self, user, userProfile):
        if userProfile.user in user.profile.following.all():
            is_following = False
            user.profile.following.remove(userProfile.user)
        else:
            if userProfile.user == user.profile.user:
                return
            is_following = True
            user.profile.following.add(userProfile.user)
        return is_following

    def follower_count(self, obj):
        return obj.user.followed_by.all().count()


    def following_count(self, obj):
        return obj.following.all().count()

    def get_following(self):
        users = self.following.all()
        return users.exclude(username=self.user.username)





class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followed_by')
    user_img = models.FileField(validators=[validate_file_extension], default="vidcraftavatar.png")
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    timestamp = models.DateField(auto_now=False, auto_now_add=True)
    profile_banner = models.FileField(validators=[validate_file_extension], default="vidcraftavatar.png")
    objects = UserProfileManager()

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('accounts:profile_detail', kwargs={'username': self.user.username})

    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = UserProfile.objects.get(id=self.id)
            if this.user_img != self.user_img:
                this.user_img.delete(save=False)
            if this.profile_banner != self.profile_banner:
                this.profile_banner.delete(save=False)
        except: pass # when new photo then we do nothing, normal case

        super(UserProfile, self).save(*args, **kwargs)


class UserMessages(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver')
    message = models.TextField()








def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        new_profile = UserProfile.objects.get_or_create(user=instance)

def post_delete_user_receiver(sender, instance, *args, **kwargs):
    instance.profile_banner.delete(False)
    instance.user_img.delete(False)

post_delete.connect(post_delete_user_receiver, sender=UserProfile)
post_save.connect(post_save_user_receiver, sender=settings.AUTH_USER_MODEL)