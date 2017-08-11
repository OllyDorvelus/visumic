__author__ = 'OllyD'


from rest_framework import generics, permissions, mixins
from .seralizers import UserDisplaySerializer, User, UserProfileSerializer, UserSeralizer, UserCreateSerializer, UserLoginSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .pagination import StandardResultsPagination
from accounts.models import UserProfile
from videos.api.serializers import VideoModelSerializer, ShareModelSerializer
from videos.models import VideoModel
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django_filters.rest_framework import DjangoFilterBackend


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

# class UserLoginAPIView(generics.APIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = UserLoginSerializer
#
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         serializer = UserLoginSerializer(data=data)
#         if serializer.is_valid(raise_exception=True):
#             new_data = serializer.data
#             return Response(new_data, status=HTTP_200_OK)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UserView(generics.ListAPIView):
    serializer_class = UserDisplaySerializer

    def get_queryset(self, *args, **kwargs):
       return User.objects.all()


class UserProfileListAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ('user__username','timestamp')
    def get_queryset(self, *args, **kwargs):
        # im_following = self.request.user.profile.get_following()
        # qs1 = UserProfile.objects.filter(user__in=im_following).order_by("user.username")
        # qs2 = UserProfile.objects.filter(user=self.request.user)
        qs = UserProfile.objects.all().order_by("user__username")
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
               # Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs

    def get_seralizer_context(self, *args, **kwargs):
        context = super(UserProfileListAPIView, self).get_seralizer_context(*args, **kwargs)
        context['request'] = self.request
        return context

class UserFollowToggleAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, username, format=None):
        userProfile_qs = UserProfile.objects.filter(user__username=username)
        message = "Not allowed"
        if request.user.is_authenticated():
            # if request.user.profile.id == userProfile_qs.first().id:
            #     return Response({"message": message}, status=400)
            is_following = UserProfile.objects.follow_toggle(request.user, userProfile_qs.first())
            follower_count = UserProfile.objects.follower_count(userProfile_qs.first())
            return Response({'following': is_following, 'follower_count': follower_count})
        return Response({"message": message}, status=400)

class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    lookup_field = "user__username"
   # def get_queryset(self, *args, **kwargs):
    def get_queryset(self, *args, **kwargs):
        qs = UserProfile.objects.all()
        return qs

class UserUpdateAPIView(mixins.UpdateModelMixin, generics.RetrieveAPIView, mixins.DestroyModelMixin):
    serializer_class = UserProfileSerializer
   # permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self, *args, **kwargs):
        qs = UserProfile.objects.all()
        return qs

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destory(request, *args, **kwargs)


class UserVideoAPIView(generics.ListAPIView):
    serializer_class = VideoModelSerializer
    pagination_class = StandardResultsPagination
    def get_queryset(self, *args, **kwargs):
        username = self.kwargs['username']
        #pk = UserProfile.objects.get(pk=pk)
        user = User.objects.get(username=username)
        qs = VideoModel.objects.filter(user_id=user.pk).order_by("-timestamp")
        return qs


class UserLikedAPIView(generics.ListAPIView):
    serializer_class = VideoModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        username = self.kwargs.get("username")
        userprofile = UserProfile.objects.get(user__username=username)
        return userprofile.user.liked.all().order_by("-timestamp")

class UserSharedAPIView(generics.ListAPIView):
    serializer_class = ShareModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        user = User.objects.get(username__iexact=self.kwargs.get("username"))
        userprofile = UserProfile.objects.get(pk=user.profile.pk)
        return userprofile.user.shared.all().order_by("-timestamp")

class UserFollowerAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    pagination_class = StandardResultsPagination
    def get_queryset(self, *args, **kwargs):
        username = self.kwargs.get("username")
        userprofile = UserProfile.objects.get(user__username=username)
        followers = userprofile.user.followed_by.all().order_by("user__username")
        return followers

class UserFollowingAPIView(generics.ListAPIView):
    serializer_class = UserSeralizer
    pagination_class = StandardResultsPagination
    def get_queryset(self, *args, **kwargs):
        username = self.kwargs.get("username")
        #user = User.objects.get(username__iexact=self.kwargs.get("username"))
        userprofile = UserProfile.objects.get(user__username=username)
        following = userprofile.following.all().order_by("username")
        return following

class FollowingVideosAPIView(generics.ListAPIView):
    serializer_class = VideoModelSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self, *args, **kwargs):
        requestuser = self.request.user
        followingusers = requestuser.profile.following.all()
        qs = VideoModel.objects.filter(user__in=followingusers).order_by("-timestamp")
        return qs




