from django.db import models
import os
from accounts.validators import validate_file_extension, validate_file_video_extension
from hitcount.models import HitCount, HitCountMixin
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import post_save, post_delete, pre_delete
import string
import random


import subprocess
from django.db.utils import IntegrityError
from django.db       import models, transaction
from django.db       import transaction
# Create your models here.
from videos.tasks import convert_video_to_mp4

# class RandomPrimaryIdModel(models.Model):
#     KEYPREFIX         = ""
#     KEYSUFFIX         = ""
#     CRYPT_KEY_LEN_MIN = 5
#     CRYPT_KEY_LEN_MAX = 9
#     _FIRSTIDCHAR      = string.ascii_letters                  # First char: Always a letter
#     _IDCHARS          = string.digits + string.ascii_letters  # Letters and digits for the rest
#
#     """ Our new ID field """
#     newid = models.CharField(db_index    = True,
#                           primary_key = True,
#                           max_length  = CRYPT_KEY_LEN_MAX+1+len(KEYPREFIX)+len(KEYSUFFIX),
#                           unique      = True)
#
#     def __str__(self, *args, **kwargs):
#         """
#         Nothing to do but to call the super class' __init__ method and initialize a few vars.
#         """
#         super(RandomPrimaryIdModel, self).__str__(*args, **kwargs)
#         self._retry_count = 0    # used for testing and debugging, nothing else
#
#     def _make_random_key(self, key_len):
#         """
#         Produce a new unique primary key.
#         This ID always starts with a letter, but can then have numbers
#         or letters in the remaining positions.
#         Whatever is specified in KEYPREFIX or KEYSUFFIX is pre/appended
#         to the generated key.
#         """
#         return self.KEYPREFIX + random.choice(self._FIRSTIDCHAR) + \
#                ''.join([ random.choice(self._IDCHARS) for dummy in range(0, key_len-1) ]) + \
#                self.KEYSUFFIX
#
#     def save(self, *args, **kwargs):
#         """
#         Modified save() function, which selects a special unique ID if necessary.
#         Calls the save() method of the first model.Models base class it can find
#         in the base-class list.
#         """
#         if self.id:
#             # Apparently, we know our ID already, so we don't have to
#             # do anything special here.
#             super(RandomPrimaryIdModel, self).save(*args, **kwargs)
#             return
#
#         try_key_len                     = self.CRYPT_KEY_LEN_MIN
#         try_since_last_key_len_increase = 0
#         while try_key_len <= self.CRYPT_KEY_LEN_MAX:
#             # Randomly choose a new unique key
#             _id = self._make_random_key(try_key_len)
#             sid = transaction.savepoint()       # Needed for Postgres, doesn't harm the others
#             try:
#                 if kwargs is None:
#                     kwargs = dict()
#                 kwargs['force_insert'] = True           # If force_insert is already present in
#                                                         # kwargs, we want to make sure it's
#                                                         # overwritten. Also, by putting it here
#                                                         # we can be sure we don't accidentally
#                                                         # specify it twice.
#                 self.id = _id
#                 super(RandomPrimaryIdModel, self).save(*args, **kwargs)
#                 break                                   # This was a success, so we are done here
#
#             except IntegrityError as e:                   # Apparently, this key is already in use
#                 # Only way to differentiate between different IntegrityErrors is to look
#                 # into the message string. Too bad. But I need to make sure I only catch
#                 # the ones for the 'id' column.
#                 #
#                 # Sadly, error messages from different databases look different and Django does
#                 # not normalize them. So I need to run more than one test. One of these days, I
#                 # could probably just examine the database settings, figure out which DB we use
#                 # and then do just a single correct test.
#                 #
#                 # Just to complicates things a bit, the actual error message is not always in
#                 # e.message, but may be in the args of the exception. The args list can vary
#                 # in length, but so far it seems that the message is always the last one in
#                 # the args list. So, that's where I get the message string from. Then I do my
#                 # DB specific tests on the message string.
#                 #
#                 msg = e.args[-1]
#                 if msg.endswith("for key 'PRIMARY'") or msg == "column id is not unique" or \
#                         "Key (id)=" in msg:
#                     transaction.savepoint_rollback(sid) # Needs to be done for Postgres, since
#                                                         # otherwise the whole transaction is
#                                                         # cancelled, if this is part of a larger
#                                                         # transaction.
#
#                     self._retry_count += 1              # Maintained for debugging/testing purposes
#                     try_since_last_key_len_increase += 1
#                     if try_since_last_key_len_increase == try_key_len:
#                         # Every key-len tries, we increase the key length by 1.
#                         # This means we only try a few times at the start, but then try more
#                         # and more for larger key sizes.
#                         try_key_len += 1
#                         try_since_last_key_len_increase = 0
#                 else:
#                     # Some other IntegrityError? Need to re-raise it...
#                     raise e
#
#         else:
#             # while ... else (just as a reminder): Execute 'else' if while loop is exited normally.
#             # In our case, this only happens if we finally run out of attempts to find a key.
#             self.id = None
#             raise IntegrityError("Could not produce unique ID for model of type %s" % type(self))
#
#     class Meta:
#         abstract = True



class VideoModelManager(models.Manager):
    use_for_related_fields = True

    def like_toggle(self, user, video_obj):
        if user in video_obj.liked.all():
            is_liked = False
            video_obj.liked.remove(user)
        else:
            is_liked = True
            video_obj.liked.add(user)
        return is_liked

    def likes_count(self, video_obj):
        return video_obj.liked.all().count()

    # def daily_views(self):
    #     return self.hit_count.hits_in_last(days=1)

    def get_queryset(self):
        return super(VideoModelManager, self).get_queryset()
    # def get_queryset(self):
    #     return super(VideoModelManager, self).get_queryset().annotate(daily_views=self.hit_count.hits_in_last(days=1))


class CommentModelManager(models.Manager):
    use_for_related_fields = True

    def like_toggle(self, user, comment_obj):
        if user in comment_obj.likedcmt.all():
            is_liked = False
            comment_obj.likedcmt.remove(user)
        else:
            is_liked = True
            comment_obj.likedcmt.add(user)
        return is_liked

    def likes_count(self, comment_obj):
        return comment_obj.likedcmt.all().count()


class PlaylistModelManager(models.Manager):
    use_for_related_fields = True

    def add_video(self, user, video, playlist_obj):
        if user == playlist_obj.user:
            in_playlist = False
            if video not in playlist_obj.videos.all():
                playlist_obj.videos.add(video)
            else:
                in_playlist = True
            return in_playlist
        else:
            return "Not your playlist"

    def remove_video(self, user, video, playlist_obj):
        if user == playlist_obj.user:
            in_playlist = True
            if video in playlist_obj.videos.all():
                playlist_obj.videos.remove(video)
            else:
                in_playlist = False
            return in_playlist
        else:
            return "Not your playlist"



class GenreModel(models.Model):
    genrename = models.CharField(max_length=100, null=False, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='category')
    is_category = models.BooleanField(verbose_name='is a category?', default=False)

    def __str__(self):
        if self.parent:
            return self.genrename + " - " + self.parent.genrename
        else:
            return self.genrename


class VideoModel(models.Model, HitCountMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, related_name='videos')
    thumbnail = models.FileField(validators=[validate_file_extension], default="vidcraftavatar.png", upload_to='thumbnails')
    video = models.FileField(upload_to="mp4video", validators=[validate_file_video_extension])
    title = models.CharField(max_length=115)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
    description = models.TextField(blank=True)
    genre = models.ForeignKey(GenreModel, on_delete=models.PROTECT, limit_choices_to={'is_category': False})
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
  #  last_edited = models.DateField(auto_now=True, auto_now_add=False)
    views = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='views')
    daily_views = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='daily_views')
    objects = VideoModelManager()


    def __str__(self):
        return self.title + '-' + self.user.username

    def get_absolute_url(self):
        return reverse('videos:video_detail', kwargs={'pk': self.pk})

    # def save(self, *args, **kwargs):
    #     video = self.video.url.replace("/", "", 1)
    #     newvideo = convert_video_to_mp4(video, "media/mp4video/" + self.title)
    #     self.video = os.path.relpath(newvideo, 'media')
    #     test = os.path.exists(self.video.url)
    #     print(test)
    #     self.title = "Hello World"
    #     super(VideoModel, self).save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #
    #     subprocess.check_call(
    #         ['ffmpeg', '-v', '-8', '-i', self.video, '-vf', 'scale=-2:480', '-preset', 'slow',
    #         '-c:v', 'libx264', '-strict', 'experimental', '-c:a', 'aac', '-crf', '20', '-maxrate', '500k',
    #         '-bufsize', '500k', '-r', '25', '-f', 'mp4', self.video, '-y'])
# def convert_video_to_mp4(video_file_path, output_name):
#   #  -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4
#     subprocess.call("ffmpeg -i {input} {output}.mp4".format(input=video_file_path, output=output_name))
#    # print(output_name + ".mp4".replace("media/", ""))
#     return output_name + ".mp4"

  #  -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4


# ready2party = VideoModel.objects.get(pk=10)
# video3 = os.path.relpath(ready2party.video.url)
# video = ready2party.video.url.replace("/", "", 1)
# video2 = "/media/mp4video/somebody.flv"
# name = "somebodywork6"
# newvideo = convert_video_to_mp4(video, "media/mp4video/" + name)
# ready2party.input_video = os.path.relpath(newvideo, 'media')
# ready2party.save()
# print(ready2party.input_video.url)
def post_save_video_receiver(sender, instance, created, *args, **kwargs):
    if created:
        convert_video_to_mp4.delay(instance)
      #   #instance.input_video = instance.video
      #   video = instance.video.url.replace("/", "", 1)
      #   #video = os.path.abspath(instance.video.url)
      #   path = instance.video.url      # newvideo = convert_video_to_mp4(video, "media/mp4video/" + instance.title
      #   filename, file_extension = os.path.splitext(instance.video.url)
      #   file_extension = file_extension.lower()
      #   if file_extension == ".mp4":
      #       filename = filename.replace("/", "", 1) + "_V"
      #   else:
      #       filename = filename.replace("/", "", 1)
      #   newvideo = convert_video_to_mp4.delay(video, filename)
      #  # instance.video.delete(save=False)
      #   instance.video = os.path.relpath(newvideo, 'media')
      #   instance.save()
      #   print("This will print to the screen first")
      # #  instance.input_video.delete(False)
      #   os.remove(video)

        #new_profile = UserProf.objects.get_or_create(user=instance)

post_save.connect(post_save_video_receiver, sender=VideoModel)
def post_delete_video_receiver(sender, instance, *args, **kwargs):

   # video = instance.video.url.replace("/", "", 1)
    #instance.video.close()
   # os.close(video)
   # os.remove(video)
    instance.video.delete(save=False)
    instance.thumbnail.delete(save=False)





post_delete.connect(post_delete_video_receiver, sender=VideoModel)

# print(os.path.relpath('myfr.jpg', 'media'))
# print(os.path.exists('media/thumbnails/myframe.jpg'))


class CommentModel(models.Model):
    video = models.ForeignKey(VideoModel, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author', on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies')
    reply = models.BooleanField(verbose_name='is a reply?', default=False)
    likedcmt = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likedcmt')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    objects = CommentModelManager()

    def __str__(self):
        return self.user.username + "-" + self.comment


class ShareModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shared')
    video = models.ForeignKey(VideoModel, related_name='shares', on_delete=models.CASCADE)
    content = models.CharField(max_length=200, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.user.username + '-' + self.content


class ShareCommentModel(models.Model):
    share = models.ForeignKey(ShareModel, related_name='sharecomments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='commentuser', on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.user.username + '-' + self.comment


class PlaylistModel(models.Model):
    name = models.CharField(max_length=200, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='playlistuser', on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    videos = models.ManyToManyField(VideoModel, related_name='playlistvideos', blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    objects = PlaylistModelManager()

    def __str__(self):
        return self.name + '-' + self.user.username

    def get_absolute_url(self):
        return reverse('videos:playlist_detail', kwargs={'pk': self.pk})

   # subprocess.call('ffmpeg -i media/mp4video/somebody.flv media/mp4video/test2.mp4')


    # def get_absolute_url(self):
    #     return reverse('accounts:profile_detail', kwargs={'username': self.user.username})

    # subprocess.check_call(
    #          ['ffmpeg', '-v', '-8', '-i', video, '-vf', 'scale=-2:480', '-preset', 'slow',
    #            '-c:v', 'libx264', '-strict', 'experimental', '-c:a', 'aac', '-crf', '20', '-maxrate', '500k',
    #            '-bufsize', '500k', '-r', '25', '-f', 'mp4', video, '-y'])

def hello_world():
    print("Hello World")

hello_world()


#convert_video_to_mp4(video, "somebodywork4")



