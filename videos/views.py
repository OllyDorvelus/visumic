from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, ListView, FormView, CreateView, UpdateView
from accounts.models import UserProfile
from .models import VideoModel, CommentModel, GenreModel, PlaylistModel
from django.contrib.auth import get_user_model
from .forms import CommentModelForm, VideoModelForm, ShareModelForm, VideoEditForm, PlaylistModelForm, PlaylistEditForm, CommentEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.contrib import messages
from .mixins import UserOwnerMixin
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from hitcount.views import HitCountDetailView
from django.conf import settings
import shutil
import os
import subprocess
User = get_user_model()
myvideo = VideoModel.objects.get(pk=14)
print(os.path.exists(myvideo.video.url.replace("/", "", 1)))
print(myvideo.video.url)
#print(os.path.abspath(myvideo.video.url))
#BOTO TESTING
# import boto
# import boto.s3
# from boto.s3.key import Key
# import sys
#
# from boto.s3.connection import S3Connection
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'AKIAIWPRIUTTARYHLUUA') #"AKIAIWPRIUTTARYHLUUA"
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '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') #"NJbxy1areLLTtuynZNiP7m8ZHZD95ftTdMlod5v6"
# AWS_STORAGE_BUCKET_NAME = 'visumic-bucket'
# REGION_HOST = 's3.us-east-2.amazonaws.com'
# bucket_name = AWS_ACCESS_KEY_ID.lower() + '-dump'
# # conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
# #         AWS_SECRET_ACCESS_KEY)
# conn2 = boto.connect_s3(AWS_ACCESS_KEY_ID,
#         AWS_SECRET_ACCESS_KEY, host=REGION_HOST)
# # bucket = conn.create_bucket(bucket_name,
# #     location=boto.s3.connection.Location.DEFAULT)
# bucket2 = conn2.get_bucket(AWS_STORAGE_BUCKET_NAME)
# samplevid = VideoModel.objects.get(pk=14)
#
# from boto.s3.key import Key
#
# import ntpath
# from boto.s3.key import Key
# def path_leaf(path):
#     head, tail = ntpath.split(path)
#     return tail or ntpath.basename(head)
# path = samplevid.video.url
# filename, file_extension = os.path.splitext(path)
# file_extension = file_extension.lower()
# print(file_extension)
# filename = 'temp/' + path_leaf(filename)
# print(filename)
# # print(os.path.abspath("temp/copyme.html"))
# testfile = os.path.abspath("temp/copyme.html") #os.path.abspath("media/mp4video/April.mkv")#
# print('Uploading %s to Amazon S3 bucket %s' % \
#    (testfile, AWS_STORAGE_BUCKET_NAME))

# def percent_cb(complete, total):
#     sys.stdout.write('.')
#     sys.stdout.flush()
# k = Key(bucket2)
# k.key = 'media/mp4video/my test html file'
# k.set_contents_from_filename(testfile,
#     cb=percent_cb, num_cb=10)
# print(k.get_contents_as_string())
# print(k.get_contents_to_filename('media/mp4video/my test html file'))
# url = k.generate_url(expires_in=0, query_auth=False, force_http=True)
# print(k)
# print(k.generate_url)
# print(os.path.normpath('thumbnails'))
# print(samplevid.video)
#END BOTO
# Create your views here.
#print(settings.MEDIA_URL)
# print('vidcraft.aws.utils.MediaRootS3BotoStorage')
# shutil.copy('temp/copyme.html', 'vidcraft.aws.utils.MediaRootS3BotoStorage')
# samplevid = VideoModel.objects.get(pk=14)
# print(str(samplevid.video))
# #path = os.path.relpath(samplevid.video.url, 'media')#os.path.relpath(samplevid.video.url, 'media')
# path = samplevid.video.url #os.path.relpath(samplevid.video.url, 'vidcraft.aws.utils.MediaRootS3BotoStorage')
# print(path)
# print(samplevid.video.url)
# filename = path
#subprocess.call("ffmpeg -re -i {input} -g 52 -ab 64k -vcodec libx264 -vb 448k -f mp4 -movflags frag_keyframe+empty_moov {output}.mp4".format(input=path, output='temp/testvideo'))
class PostCountHitDetailView(HitCountDetailView):
    model = VideoModel        # your model goes here
    count_hit = True

class VideoDetailView(PostCountHitDetailView, HitCountMixin):

    model = VideoModel
    qs = VideoModel.objects.all()
    template_name = "videos/video_detail.html"
    context_object_name = "video"

    #
    # def hit_count(self, *args, **kwargs):
    #     hit_count = HitCount.objects.get_for_object(VideoModel)
    #     hit_count_response = HitCountMixin.hit_count(self.request, hit_count)
    #
    #     return hit_count_response
    # def get_object(self):
    #     return get_object_or_404(VideoModel, pk=pk)

    def get_context_data(self, *args, **kwargs):
        #user = super(UserDetailView, self).get_object(self, *args, **kwargs)
        #video = VideoDetailView.get_object(self)
        context = super(VideoDetailView, self).get_context_data(*args, **kwargs)
        #context['all_comments'] = CommentModel.objects.filter(video=video)
        context['comment_form'] = CommentModelForm
        context['comment_url'] = reverse_lazy("accounts:home")
        context['share_form'] = ShareModelForm
        context['share_url'] = reverse_lazy("accounts:home")
        context['video_edit_form'] = VideoEditForm
        context['playlist_create_form'] = PlaylistModelForm
        context['video_url'] = reverse_lazy("accounts:home")
        context['comment_edit_form'] = CommentEditForm
        context['comment_url'] = reverse_lazy("accounts:home")
        return context




class VideoListView(ListView):
    model = VideoModel
    template_name = "videos/video_list.html"
    context_object_name = "videos"

    def get_queryset(self):
        return VideoModel.objects.all()

class PlaylistListView(ListView):
    model = PlaylistModel
    template_name = "videos/playlist_list.html"
    context_object_name = "playlist"

    def get_queryset(self):
        return PlaylistModel.objects.all()

class VideoGenreListView(DetailView):
    model = GenreModel
    template_name = "videos/video_genre_list.html"
    context_object_name = "genre"
    #slug_field = 'genrename'

    def get_object(self):
        # categories = GenreModel.objects.filter(is_category=True)
        # category = self.kwargs.get("category")
        # category = categories.get(genrename__iexact=category)
        # genre = self.kwargs.get("genrename")
        # genre = GenreModel.objects.get(genrename__iexact=genre)
        genre = get_object_or_404(GenreModel, genrename__iexact=self.kwargs.get("genrename"))
        return genre

    def get_context_data(self, *args, **kwargs):
        context = super(VideoGenreListView, self).get_context_data(*args, **kwargs)
        context['parent'] = self.kwargs.get("category")
        genre = get_object_or_404(GenreModel, genrename__iexact=self.kwargs.get("genrename"))
        genres = GenreModel.objects.filter(parent_id=genre.parent.pk)
        context['genres'] = genres
        return context


class VideoCategoryListView(DetailView):
    model = GenreModel
    template_name = "videos/video_category_list.html"
    context_object_name = "category"
    #slug_field = 'genrename'

    def get_object(self):
        categories = GenreModel.objects.filter(is_category=True)
        genre = get_object_or_404(categories, genrename__iexact=self.kwargs.get("category"))
        return genre

    def get_context_data(self, *args, **kwargs):
        context = super(VideoCategoryListView, self).get_context_data(*args, **kwargs)
        category = self.kwargs.get("category")
        category = GenreModel.objects.get(genrename__iexact=category)
        genres = GenreModel.objects.filter(parent_id=category.pk)
        context['genres'] = genres
        return context

class VideoUploadView(CreateView):
    model = VideoModel
    #fields=['video']
    form_class = VideoModelForm
    template_name = "videos/video_upload.html"

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("accounts:home")
        else:
            return super(VideoUploadView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(VideoUploadView, self).form_valid(form)

class VideoUpdateView(UpdateView, LoginRequiredMixin, UserOwnerMixin):
    template_name = "videos/video_edit.html"
    model = VideoModel
    fields = ['title', 'thumbnail', 'description', 'genre']



    def get_object(self, *args, **kwargs):
        pk = self.kwargs['pk']
        video = VideoModel.objects.get(pk=pk)
        return video

    def dispatch(self, request, *args, **kwargs):
        video = VideoUpdateView.get_object(self)
        if not request.user.is_authenticated:
            return redirect("accounts:home")
        if video.user != self.request.user:
            return redirect("accounts:home")
        else:
            return super(VideoUpdateView, self).dispatch(request, *args, **kwargs)



    def form_valid(self, form, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, 'Video Updated!')
        return super(VideoUpdateView, self).form_valid(form, *args, **kwargs)


class PlaylistDetailView(DetailView):
    model = PlaylistModel
    qs = PlaylistModel.objects.all()
    template_name = "videos/playlist_detail.html"
    context_object_name = "playlist"

    def get_context_data(self, *args, **kwargs):
        context = super(PlaylistDetailView, self).get_context_data(*args, **kwargs)
        context['playlist_edit_form'] = PlaylistEditForm
        context['playlist_url'] = reverse_lazy("accounts:home")
        return context
