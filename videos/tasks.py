# Create your tasks here
from __future__ import absolute_import
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import task, periodic_task
import subprocess
import os
from django.conf import settings
import shutil
from random import randint
from datetime import timedelta


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


@task(name="convert_video_to_mp4")
def convert_video_to_mp4(instance):
  #  -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4

   # print(output_name + ".mp4".replace("media/", ""))
        #instance.input_video = instance.video

    video = instance.video.url#.replace("/", "", 1)

    #video = os.path.abspath(instance.video.url)
    path = instance.video.url      # newvideo = convert_video_to_mp4(video, "media/mp4video/" + instance.title
    filename, file_extension = os.path.splitext(instance.video.url)
    file_extension = file_extension.lower()
    if file_extension == ".mp4":
        filename = filename + "_V" #.replace("/", "", 1) + "_V"
    else:
        filename = filename #.replace("/", "", 1)
    subprocess.call("ffmpeg -i {input} -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4  {output}.mp4".format(input=video, output=filename))
    newvideo = filename + ".mp4"
    # instance.video.delete(save=False)
    instance.video = os.path.relpath(newvideo, 'media')
    title = instance.title
    title = title.replace(" ", "_")
    title = title + "" + str(randint(0, 100000))
   # print(title)
   # print(video)
    subprocess.call("ffmpeg -i {video} -ss 00:00:20 -t 00:00:1 -s 1080x720 -r 1 -f singlejpeg {thumbnail}.jpg".format(video=newvideo, thumbnail=title))
    thumbnail = title + ".jpg"
    shutil.move(thumbnail, 'media/thumbnails/')
   # os.rename(title, '/media/thumbnails')
    instance.thumbnail = os.path.normpath('thumbnails/' + thumbnail)
    instance.save()
    print("This will print to the screen first")
    #  instance.input_video.delete(False)
    os.remove(video)
    return instance



