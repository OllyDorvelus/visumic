__author__ = 'OllyD'


from rest_framework import generics, permissions, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
#from .seralizers import UserDisplaySerializer, User, UserProfileSerializer
from .serializers import (VideoModelSerializer, CommentModelSerializer, ShareModelSerializer, VideoModelEditSerializer, ShareModelCommentSerializer,
                          PlaylistModelSerializer)
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .pagination import StandardResultsPagination, StandardResultsPagination2, RelatedResultsPagination, ShareResultsPagination
from accounts.models import UserProfile
from videos.models import VideoModel, CommentModel, ShareModel, ShareCommentModel, GenreModel, PlaylistModel
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .permissions import MyUserPermissions, UserAddOrRemovePermissions, UserAndVideoUserPermissions
from videos.tasks import random_vid_day
example = 0
User = get_user_model()




# import schedule
# import time
#
# def job(t):
#     print("I'm working...", t)
#     return
#
# schedule.every().day.at("01:00").do(job,'It is 01:00')
#
# while True:
#     schedule.run_pending()
#     time.sleep(60) # wait one minute

from datetime import datetime
from threading import Timer
print("Okay")
x=datetime.today()
#y=x.replace(day=x.day+1, hour=0, minute=8, second=0, microsecond=0)
y=x.replace(day=x.day, hour=0, minute=9, second=0, microsecond=0)
delta_t=y-x

secs=delta_t.seconds+1
randomvid = VideoModel.objects.all().order_by('?')[:1]
randomvid2 = random_vid_day()
def hello_world():
    print("Hello World")
    global randomvid
    randomvid = VideoModel.objects.all().order_by('?')[:1]

t = Timer(secs, hello_world)
t.start()


class VideoModelListAPIView(generics.ListAPIView):

    serializer_class = VideoModelSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ('title','timestamp')
    #search_fields = ['title', 'timestamp']
    def get_queryset(self, *args, **kwargs):

        # im_following = self.request.user.profile.get_following()
        # qs1 = UserProfile.objects.filter(user__in=im_following).order_by("user.username")
        # qs2 = UserProfile.objects.filter(user=self.request.user)
        qs = VideoModel.objects.all().order_by('-timestamp')
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(user__username__icontains=query) |
                Q(description__icontains=query)
            )
        return qs

    def get_seralizer_context(self, *args, **kwargs):
        context = super(VideoModelSerializer, self).get_seralizer_context(*args, **kwargs)
        context['request'] = self.request
        return context

class RelatedListAPIView(generics.ListAPIView):
    serializer_class = VideoModelSerializer
    pagination_class = RelatedResultsPagination

    def get_queryset(self, *args, **kwargs):
        video = self.kwargs['video']
        video = VideoModel.objects.get(pk=video)
        title = video.title
        description = video.description
        genrename = video.genre.genrename
        qs = VideoModel.objects.all().order_by('timestamp').exclude(pk=video.pk)
        qs = qs.filter(
            Q(title__iregex=r"\y{0}\y".format(title))
          | Q(genre__genrename__icontains=genrename)
        )
        # qs = qs.filter(
        #     Q(title__icontains=r'^[april]+/$') #|
        #    # Q(description__icontains=description)
        # )
        #         qs = qs.filter(
        #     Q(title__iregex=r"\y{0}\y".format(title)) #|
        #    # Q(description__icontains=description)
        # )
        return qs


class RandomVideoAPIView(generics.ListAPIView):
    serializer_class= VideoModelSerializer

    def get_queryset(self):
        #qs = VideoModel.objects.all().order_by('?')[:1]
       # return random_vid_day.delay()
        return VideoModel.objects.get(pk=20)
        #global randomvid2
        #return random_vid_day

class VideoModelDetailAPIView(mixins.DestroyModelMixin, mixins.UpdateModelMixin, generics.RetrieveAPIView):
    serializer_class = VideoModelSerializer
    queryset = VideoModel.objects.all()
    permission_classes = [MyUserPermissions]

    # def get_queryset(self, *args, **kwargs):
    #     qs = get_object_or_404(VideoModel, pk=self.pk)
    #     return qs

    def get_seralizer_context(self, *args, **kwargs):
        context = super(VideoModelSerializer, self).get_seralizer_context(*args, **kwargs)
        context['request'] = self.request
        return

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(self, request, *args, **kwargs)

    # def has_object_permission(self, request, view, obj):
    #
    #     # check if user is owner
    #     return request.user == obj.user

class VideoModelUpdateAPIView(mixins.UpdateModelMixin,generics.RetrieveAPIView,):
    serializer_class = VideoModelEditSerializer
    permission_classes = [permissions.IsAuthenticated, MyUserPermissions]

    queryset = VideoModel.objects.filter(id__gte=0)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)



    def get_seralizer_context(self, *args, **kwargs):
        context = super(VideoModelEditSerializer, self).get_seralizer_context(*args, **kwargs)
        context['request'] = self.request
        return context


    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class VideoModelDeleteAPIView(generics.DestroyAPIView):
    serializer_class = VideoModelEditSerializer
  #  permission_classes = [permissions.IsAuthenticated, MyUserPermissions]
    queryset = VideoModel.objects.all()

class CommentModelDetailAPIView(generics.RetrieveAPIView, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    serializer_class = CommentModelSerializer
    queryset = CommentModel.objects.all()
    permission_classes = [UserAndVideoUserPermissions]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)






class CommentModelListAPIView(generics.ListAPIView):
    serializer_class = CommentModelSerializer
    pagination_class = StandardResultsPagination
    def get_queryset(self, *args, **kwargs):
        video = self.kwargs['video']
        qs = CommentModel.objects.filter(video=video).order_by('-timestamp')
        return qs

class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentModelSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer, *args, **kwargs):
        video = self.kwargs['video']
        comment_video = VideoModel.objects.get(pk=video)
        serializer.save(user=self.request.user, video=comment_video)

class ReplyCommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentModelSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer, *args, **kwargs):
        # video = self.kwargs['video']
        pk = self.kwargs['pk']
        comment_parent = CommentModel.objects.get(pk=pk)
        comment_video = comment_parent.video
        serializer.save(user=self.request.user, video=comment_video, parent=comment_parent, reply=True)


class CommentModelReplyListAPIView(generics.ListAPIView):
    serializer_class = CommentModelSerializer
    pagination_class = StandardResultsPagination2
    def get_queryset(self, *args, **kwargs):
        # video = self.kwargs['video']
        pk = self.kwargs['pk']

        comment = CommentModel.objects.get(pk=pk)
        qs = comment.replies.all().order_by('timestamp')
        return qs

class VideoLikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, format=None):
        video_qs = VideoModel.objects.filter(pk=pk)
        message = "Not allowed"
        if request.user.is_authenticated():
            is_liked = VideoModel.objects.like_toggle(request.user, video_qs.first())
            likes_count = VideoModel.objects.likes_count(video_qs.first())
            return Response({'liked': is_liked, 'likes_count': likes_count})
        return Response({"message": message}, status=400)


class AddVideoToPlaylistAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, id, format=None):
        video_qs = VideoModel.objects.filter(pk=id)
        playlist_qs = PlaylistModel.objects.filter(pk=pk)
        message = "Not allowed"
        if request.user.is_authenticated():
            in_playlist = PlaylistModel.objects.add_video(request.user, video_qs.first(), playlist_qs.first())
            likes_count = VideoModel.objects.likes_count(video_qs.first())
            return Response({'in_playlist': in_playlist, 'likes_count': likes_count})
        return Response({"message": message}, status=400)

class RemoveVideoToPlaylistAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, id, format=None):
        video_qs = VideoModel.objects.filter(pk=id)
        playlist_qs = PlaylistModel.objects.filter(pk=pk)
        message = "Not allowed"
        if request.user.is_authenticated():
            in_playlist = PlaylistModel.objects.remove_video(request.user, video_qs.first(), playlist_qs.first())
            likes_count = VideoModel.objects.likes_count(video_qs.first())
            return Response({'in_playlist': in_playlist, 'likes_count': likes_count})
        return Response({"message": message}, status=400)

class CommentLikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, format=None):
        comment_qs = CommentModel.objects.filter(pk=pk)
        message = "Not allowed"
        if request.user.is_authenticated():
            is_liked = CommentModel.objects.like_toggle(request.user, comment_qs.first())
            likes_count = CommentModel.objects.likes_count(comment_qs.first())
            return Response({'liked': is_liked, 'likes_count': likes_count})
        return Response({"message": message}, status=400)

class ShareListAPIView(generics.ListAPIView):
    serializer_class = ShareModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        video = self.kwargs['video']
        qs = ShareModel.objects.filter(video=video).order_by('-timestamp')
        return qs

class ShareDetailAPIView(generics.RetrieveAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = ShareModelSerializer
    queryset = ShareModel.objects.all()
    permission_classes = [MyUserPermissions]

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ShareCreateAPIView(generics.CreateAPIView):
    serializer_class = ShareModelSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer, *args, **kwargs):
        video = self.kwargs['video']
        shared_video = VideoModel.objects.get(pk=video)
        serializer.save(user=self.request.user, video=shared_video)

class VideoModelRecentAPIView(generics.ListAPIView):
    serializer_class = VideoModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        return VideoModel.objects.all().order_by("-timestamp")


class ShareCommentModelListAPIView(generics.ListAPIView):
    serializer_class = ShareModelCommentSerializer
    pagination_class = StandardResultsPagination
    def get_queryset(self, *args, **kwargs):
        share = self.kwargs['share']
        qs = ShareCommentModel.objects.filter(share=share).order_by('-timestamp')
        return qs

class ShareFollowingAPIView(generics.ListAPIView):
    serializer_class = ShareModelSerializer
    pagination_class = ShareResultsPagination
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self, *args, **kwargs):
        requestuser = self.request.user
        followingusers = requestuser.profile.following.all()
       # qs = ShareModel.objects.filter(user__in=followingusers)
        qs = ShareModel.objects.filter(Q(user__in=followingusers) | Q(user=requestuser)).order_by("-timestamp")
        return qs



class VideoGenreAPIView(generics.ListAPIView):
    serializer_class = VideoModelSerializer
    pagination_class = StandardResultsPagination
    def get_queryset(self, *args, **kwargs):
        genrename = GenreModel.objects.get(genrename__iexact=self.kwargs.get("genrename"))
        qs = VideoModel.objects.filter(genre_id=genrename.pk)

        # im_following = self.request.user.profile.get_following()
        # qs1 = UserProfile.objects.filter(user__in=im_following).order_by("user.username")
        # qs2 = UserProfile.objects.filter(user=self.request.user)
        # query = self.request.GET.get("q", None)
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(user__username__icontains=query) |
                Q(description__icontains=query)
            )
        return qs

class VideoNewGenreAPIView(generics.ListAPIView):
    serializer_class = VideoModelSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ('title','timestamp')
    def get_queryset(self, *args, **kwargs):
        categories = GenreModel.objects.filter(is_category=True)
        category = self.kwargs.get("category")
        category = categories.get(genrename__iexact=category)
        genre = self.kwargs.get("genrename")
        genre = GenreModel.objects.get(genrename__iexact=genre)
       # genre = categories.get(genrename__iexact=self.kwargs.get("category"))

        videos = VideoModel.objects.filter(genre__parent_id=category.pk)
        qs = videos.filter(genre_id=genre.pk).order_by("-timestamp")


        # im_following = self.request.user.profile.get_following()
        # qs1 = UserProfile.objects.filter(user__in=im_following).order_by("user.username")
        # qs2 = UserProfile.objects.filter(user=self.request.user)
        # query = self.request.GET.get("q", None)
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(user__username__icontains=query) |
                Q(description__icontains=query)
            )
        return qs

class VideoCategoryAPIView(generics.ListAPIView):
    serializer_class = VideoModelSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ('title','timestamp')
    def get_queryset(self, *args, **kwargs):
        categories = GenreModel.objects.filter(is_category=True)
        genre = categories.get(genrename__iexact=self.kwargs.get("genrename"))
        qs = VideoModel.objects.filter(genre__parent_id=genre.pk).order_by("-timestamp")

        # im_following = self.request.user.profile.get_following()
        # qs1 = UserProfile.objects.filter(user__in=im_following).order_by("user.username")
        # qs2 = UserProfile.objects.filter(user=self.request.user)
        # query = self.request.GET.get("q", None)
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(user__username__icontains=query) |
                Q(description__icontains=query)
            )
        return qs





class PlaylistListAPIView(generics.ListAPIView):
    serializer_class = PlaylistModelSerializer
    pagination_class = StandardResultsPagination
    def get_queryset(self, *args, **kwargs):

        # im_following = self.request.user.profile.get_following()
        # qs1 = UserProfile.objects.filter(user__in=im_following).order_by("user.username")
        # qs2 = UserProfile.objects.filter(user=self.request.user)
        qs = PlaylistModel.objects.all().order_by('timestamp')
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(user__username__icontains=query) |
                Q(description__icontains=query)
            )
        return qs

    def get_seralizer_context(self, *args, **kwargs):
        context = super(PlaylistModelSerializer, self).get_seralizer_context(*args, **kwargs)
        context['request'] = self.request
        return context


class PlaylistDetailAPIView(generics.RetrieveAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    permission_classes = [MyUserPermissions]
    serializer_class = PlaylistModelSerializer
    queryset = PlaylistModel.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class UserPlaylistAPIView(generics.ListAPIView, mixins.UpdateModelMixin, generics.RetrieveAPIView):
    serializer_class = PlaylistModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        user = User.objects.get(username__iexact=self.kwargs.get("username"))
        qs = PlaylistModel.objects.filter(user=user).order_by("name")
        return qs

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class PlaylistVideosAPIView(generics.ListAPIView):
    serializer_class = VideoModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs['pk']
        playlist = PlaylistModel.objects.get(pk=pk)
        qs = playlist.videos.all()
        return qs


class PlaylistCreateAPIView(generics.CreateAPIView):
    serializer_class = PlaylistModelSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(user=self.request.user)
