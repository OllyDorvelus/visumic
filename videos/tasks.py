# Create your tasks here
from __future__ import absolute_import
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import task, periodic_task
import subprocess
import os
import sys
from django.conf import settings
import shutil
from random import randint
from datetime import timedelta
import boto
import boto.s3
import ntpath
from boto.s3.key import Key
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)



AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'AKIAIWPRIUTTARYHLUUA') #"AKIAIWPRIUTTARYHLUUA"
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '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') #"NJbxy1areLLTtuynZNiP7m8ZHZD95ftTdMlod5v6"
AWS_STORAGE_BUCKET_NAME = 'visumic-bucket'
REGION_HOST = 's3.us-east-2.amazonaws.com'

conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY, host=REGION_HOST)
bucket = conn.get_bucket(AWS_STORAGE_BUCKET_NAME)
print(bucket.list())

def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

@task(name="convert_video_to_mp4")
def convert_video_to_mp4(instance_id):
  #  -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4

   # print(output_name + ".mp4".replace("media/", ""))
        #instance.input_video = instance.video
    from videos.models import VideoModel
    instance = VideoModel.objects.get(pk=instance_id)
    video = instance.video.url.replace("/", "", 1)
    #video = 'temp/April.mkv'
    #video = os.path.abspath(instance.video.url)
    path = instance.video.url      # newvideo = convert_video_to_mp4(video, "media/mp4video/" + instance.title
    filename, file_extension = os.path.splitext(video)#instance.video.url)
    norm_file_extension = file_extension
    file_extension = file_extension.lower()
    filename = 'temp/' + path_leaf(filename).replace('/app/', '')# uncomment
   # video = '//s3.us-east-2.amazonaws.com/visumic-bucket/media/mp4video/Nas_-_Cherry_Wine_Explicit_ft._Amy_Winehouse.mp4'
   # video = 'mp4video/' + path_leaf(filename) + file_extension
    if file_extension == ".mp4":
        filename = filename#.replace("/", "", 1) + "_V"
    else:
        filename = filename#.replace("/", "", 1)
   # subprocess.call("ffmpeg -i {input} {output}.mp4".format(input=video, output=filename))
      #-f mp4 -movflags frag_keyframe+empty_moov
    subprocess.call("ffmpeg -re -i {input} -f mp4 {output}.mp4".format(input=video, output=filename), shell=True)
    newvideo = filename + ".mp4"
    newvideoname = newvideo.replace("temp/", "")
    videofile = os.path.abspath(newvideo).replace('/app/', '')
    # videoKey = Key(bucket)
    # videoKey.key = 'media/mp4video/' + newvideoname
    # videoKey.set_contents_from_filename(videofile,
    # cb=percent_cb, num_cb=10)
    # instance.video.delete(save=False)
    # instance.video = 'mp4video/' + newvideoname
    # instance.video.delete(save=False)
   # instance.video = os.path.relpath(newvideo, 'media')
    if instance.thumbnail == "vidcraftavatar.png":
        title = instance.title
        title = title.replace(" ", "_")
        title = 'temp/' + title + "" + str(randint(0, 100000))
       # print(title)
       # print(video)
        subprocess.call("ffmpeg -i {video} -ss 00:00:20 -t 00:00:1 -s 1080x720 -r 1 -f singlejpeg {thumbnail}.jpg".format(video=newvideo, thumbnail=title))
        thumbnail = title + ".jpg"
        thumbnailname = thumbnail.replace("temp/", "")
        thumbnailfile = os.path.abspath(thumbnail)
        thumbnailKey = Key(bucket)
        thumbnailKey.key = 'media/thumbnails/' + thumbnailname
        thumbnailKey.set_contents_from_filename(thumbnailfile,
            cb=percent_cb, num_cb=10)
        #shutil.move(thumbnail, 'media/thumbnails/')
       # os.rename(title, '/media/thumbnails')
        instance.thumbnail = 'thumbnails/' + thumbnailname
        #instance.thumbnail = os.path.normpath('thumbnails/' + thumbnail)

    #instance.save() uncomm
    print("This will print to the screen first")
    #  instance.input_video.delete(False)
   # video = newvideoname.replace(".mp4", norm_file_extension)
   # video = "media/mp4video/" + video
    #os.remove(newvideo) uncomm
    #os.remove(thumbnail) uncomm
   # os.remove(video)
    return instance
# @task(name="convert_video_to_mp4")
# def convert_video_to_mp4(instance, video_file_path, output_name):
#   #  -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4
#     subprocess.call("ffmpeg -i {input} {output}.mp4".format(input=video_file_path, output=output_name))
#    # print(output_name + ".mp4".replace("media/", ""))
#         #instance.input_video = instance.video
#         video = instance.video.url.replace("/", "", 1)
#         #video = os.path.abspath(instance.video.url)
#         path = instance.video.url      # newvideo = convert_video_to_mp4(video, "media/mp4video/" + instance.title
#         filename, file_extension = os.path.splitext(instance.video.url)
#         file_extension = file_extension.lower()
#         if file_extension == ".mp4":
#             filename = filename.replace("/", "", 1) + "_V"
#         else:
#             filename = filename.replace("/", "", 1)
#         newvideo = convert_video_to_mp4.delay(video, filename)
#        # instance.video.delete(save=False)
#         instance.video = os.path.relpath(newvideo, 'media')
#         instance.save()
#         print("This will print to the screen first")
#       #  instance.input_video.delete(False)
#         os.remove(video)
#     return output_name + ".mp4"

@periodic_task(
    run_every=(timedelta(seconds=10)),
    name="random_vid_day",
)
def random_vid_day():
        from videos.models import VideoModel
        return VideoModel.objects.all().order_by('?')[:1]


@task(name='subtract')
def subtract(x,y):
    return y-x


# @task(name="convert_video_to_mp4")
# def convert_video_to_mp4(instance):
#   #  -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4
#
#    # print(output_name + ".mp4".replace("media/", ""))
#         #instance.input_video = instance.video
#
#     video = instance.video.url#.replace("/", "", 1)
#
#     #video = os.path.abspath(instance.video.url)
#     path = instance.video.url      # newvideo = convert_video_to_mp4(video, "media/mp4video/" + instance.title
#     filename, file_extension = os.path.splitext(instance.video.url)
#     file_extension = file_extension.lower()
#     if file_extension == ".mp4":
#         filename = filename + "_V" #.replace("/", "", 1) + "_V"
#     else:
#         filename = filename #.replace("/", "", 1)
#     subprocess.call("ffmpeg -re -i {input} -g 52 -ab 64k -vcodec libx264 -vb 448k -f mp4 -movflags frag_keyframe+empty_moov {output}.mp4".format(input=video, output=filename))
#     newvideo = filename + ".mp4"
#     # instance.video.delete(save=False)
#     instance.video = os.path.relpath(newvideo, 'media')
#     title = instance.title
#     title = title.replace(" ", "_")
#     title = title + "" + str(randint(0, 100000))
#    # print(title)
#    # print(video)
#     subprocess.call("ffmpeg -i {video} -ss 00:00:20 -t 00:00:1 -s 1080x720 -r 1 -f singlejpeg {thumbnail}.jpg".format(video=newvideo, thumbnail=title))
#     thumbnail = title + ".jpg"
#     shutil.move(thumbnail, 'media/thumbnails/')
#    # os.rename(title, '/media/thumbnails')
#     instance.thumbnail = os.path.normpath('thumbnails/' + thumbnail)
#     instance.save()
#     print("This will print to the screen first")
#     #  instance.input_video.delete(False)
#     os.remove(video)
#     return instance



# @task(name="convert_video_to_mp4")
# def convert_video_to_mp4(instance):
#   #  -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4
#
#    # print(output_name + ".mp4".replace("media/", ""))
#         #instance.input_video = instance.video
#
#     video = str(instance.video)#.replace("/", "", 1)
#
#     #video = os.path.abspath(instance.video.url)
#     path = instance.video      # newvideo = convert_video_to_mp4(video, "media/mp4video/" + instance.title
#     # filename, file_extension = os.path.splitext(instance.video)
#     # file_extension = file_extension.lower()
#     file_extension = ""
#     filename = str(instance.video)
#     if file_extension == ".mp4":
#         filename = filename + "_V" #.replace("/", "", 1) + "_V"
#     else:
#         filename = filename #.replace("/", "", 1)
#     subprocess.call("ffmpeg -re -i {input} -g 52 -ab 64k -vcodec libx264 -vb 448k -f mp4 -movflags frag_keyframe+empty_moov {output}.mp4".format(input=video, output=filename))
#     newvideo = filename + ".mp4"
#     # instance.video.delete(save=False)
#     instance.video = os.path.relpath(newvideo, 'media')
#     title = instance.title
#     title = title.replace(" ", "_")
#     title = title + "" + str(randint(0, 100000))
#    # print(title)
#    # print(video)
#     subprocess.call("ffmpeg -i {video} -ss 00:00:20 -t 00:00:1 -s 1080x720 -r 1 -f singlejpeg {thumbnail}.jpg".format(video=newvideo, thumbnail=title))
#     thumbnail = title + ".jpg"
#     shutil.move(thumbnail, 'media/thumbnails/')
#    # os.rename(title, '/media/thumbnails')
#     instance.thumbnail = os.path.normpath('thumbnails/' + thumbnail)
#     instance.save()
#     print("This will print to the screen first")
#     #  instance.input_video.delete(False)
#     os.remove(video)
#     return instance

#PRODUCTION TASK

# @task(name="convert_video_to_mp4")
# def convert_video_to_mp4(instance):
#   #  -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4
#
#    # print(output_name + ".mp4".replace("media/", ""))
#         #instance.input_video = instance.video
#
#     video = instance.video.url.replace("/", "", 1)
#
#     #video = os.path.abspath(instance.video.url)
#     path = instance.video.url      # newvideo = convert_video_to_mp4(video, "media/mp4video/" + instance.title
#     filename, file_extension = os.path.splitext(instance.video.url)
#     file_extension = file_extension.lower()
#     if file_extension == ".mp4":
#         filename = filename#.replace("/", "", 1) + "_V"
#     else:
#         filename = filename#.replace("/", "", 1)
#    # subprocess.call("ffmpeg -i {input} {output}.mp4".format(input=video, output=filename))
#     subprocess.call("ffmpeg -re -i {input} -f mp4 -movflags frag_keyframe+empty_moov -f mp4 {output}.mp4".format(input=video, output=filename))
#     newvideo = filename + ".mp4"
#     # instance.video.delete(save=False)
#     instance.video = os.path.relpath(newvideo, 'media')
#     if instance.thumbnail == "vidcraftavatar.png":
#         title = instance.title
#         title = title.replace(" ", "_")
#         title = title + "" + str(randint(0, 100000))
#        # print(title)
#        # print(video)
#         subprocess.call("ffmpeg -i {video} -ss 00:00:20 -t 00:00:1 -s 1080x720 -r 1 -f singlejpeg {thumbnail}.jpg".format(video=newvideo, thumbnail=title))
#         thumbnail = title + ".jpg"
#         shutil.move(thumbnail, 'media/thumbnails/')
#        # os.rename(title, '/media/thumbnails')
#         instance.thumbnail = os.path.normpath('thumbnails/' + thumbnail)
#     instance.save()
#     print("This will print to the screen first")
#     #  instance.input_video.delete(False)
#     os.remove(video)
#     return instance
#END PRODUCTION TASK
# ORIGINAL WORKING ON LOCAL

# @task(name="convert_video_to_mp4")
# def convert_video_to_mp4(instance):
#   #  -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4
#
#    # print(output_name + ".mp4".replace("media/", ""))
#         #instance.input_video = instance.video
#
#     video = instance.video.url.replace("/", "", 1)
#
#     #video = os.path.abspath(instance.video.url)
#     path = instance.video.url      # newvideo = convert_video_to_mp4(video, "media/mp4video/" + instance.title
#     filename, file_extension = os.path.splitext(instance.video.url)
#     file_extension = file_extension.lower()
#     if file_extension == ".mp4":
#         filename = filename.replace("/", "", 1) + "_V"
#     else:
#         filename = filename.replace("/", "", 1)
#     subprocess.call("ffmpeg -i {input} {output}.mp4".format(input=video, output=filename))
#     newvideo = filename + ".mp4"
#     # instance.video.delete(save=False)
#     instance.video = os.path.relpath(newvideo, 'media')
#     if instance.thumbnail == "vidcraftavatar.png":
#         title = instance.title
#         title = title.replace(" ", "_")
#         title = title + "" + str(randint(0, 100000))
#        # print(title)
#        # print(video)
#         subprocess.call("ffmpeg -i {video} -ss 00:00:20 -t 00:00:1 -s 1080x720 -r 1 -f singlejpeg {thumbnail}.jpg".format(video=newvideo, thumbnail=title))
#         thumbnail = title + ".jpg"
#         shutil.move(thumbnail, 'media/thumbnails/')
#        # os.rename(title, '/media/thumbnails')
#         instance.thumbnail = os.path.normpath('thumbnails/' + thumbnail)
#     instance.save()
#     print("This will print to the screen first")
#     #  instance.input_video.delete(False)
#     os.remove(video)
#     return instance