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
import os

User = get_user_model()
# Create your views here.

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
