from django.db import models
from django.conf import settings
from django.urls import reverse
from localflavor.us.models import USStateField
from django.db.models.signals import post_save, post_delete
from accounts.validators import validate_file_extension
from notifications.signals import notify
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()
class EventModelManager(models.Manager):
    use_for_related_fields = True

    def attending_count(self, event_obj):
        return event_obj.attending.all().count()

    def attend_toggle(self, user, event_obj):
        if user in event_obj.attending.all():
            is_attending = False
            event_obj.attending.remove(user)
        else:
            is_attending = True
            event_obj.attending.add(user)
            if user != event_obj.user:
                notify.send(user, recipient=event_obj.user, verb=' is attending your event: ' + event_obj.name, target=event_obj)
        return is_attending



class EventModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, related_name='events')
    name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=100)
    state = USStateField()
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=5)
    picture = models.FileField(validators=[validate_file_extension], upload_to='event_pictures')
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    attending = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='attend')
    objects = EventModelManager()

    def __str__(self):
        return self.user.username + '-' + self.name

    def get_absolute_url(self):
        return reverse('events:event_detail', kwargs={'pk': self.pk})

def post_save_event_receiver(sender, instance, *args, **kwargs):
        user = User.objects.get(pk=instance.user.pk)
        followers = user.followed_by.all()
        followers = User.objects.filter(profile__in=followers)
        notify.send(instance.user, recipient=followers, verb=" created an event: " + instance.name, target=instance)
post_save.connect(post_save_event_receiver, sender=EventModel)

def post_delete_event_receiver(sender, instance, *args, **kwargs):

        if instance.picture != "vidcraftavatar.png" and instance.picture != "vthumbnail.jpg":
            instance.picture.delete(save=False)
post_delete.connect(post_delete_event_receiver, sender=EventModel)