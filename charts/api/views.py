from django.db.models import Q, Min, Count
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from videos.models import VideoModel, GenreModel

from videos.api.pagination import StandardResultsPagination, ChartResultsPagination
from videos.api.serializers import VideoModelSerializer


from hashtags.models import HashTagModel
randomvid = VideoModel.objects.all().order_by('?')[:1]
class AllTimeAPIView(generics.ListAPIView):
    filter_backends = [SearchFilter, OrderingFilter]
    order_fields = ['views']
   # search_fields = ['genre__parent__genrename']
    serializer_class = VideoModelSerializer
    pagination_class = ChartResultsPagination
   # queryset = VideoModel.objects.all().order_by('views')[:100]


    def get_queryset(self, *args, **kwargs):
        # im_following = self.request.user.profile.get_following()
        # qs1 = UserProfile.objects.filter(user__in=im_following).order_by("user.username")
        # qs2 = UserProfile.objects.filter(user=self.request.user)
        categories = GenreModel.objects.filter(is_category=True)
        category = self.kwargs.get("category")
        category = categories.get(genrename__iexact=category)
        qs = VideoModel.objects.filter(genre__parent_id=category.pk).order_by('views')
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(genre__genrename__icontains=query)# |
               # Q(genre__parent__genrename__icontains=query)
            )
        return qs[:100]

class DailyAPIView(generics.ListAPIView):
    filter_backends = [SearchFilter, OrderingFilter]
    filter_fields = ('title', 'video', 'views', 'wsfs')
    #queryset = VideoModel.objects.all().order_by("views")[:100]
    queryset = VideoModel.objects.all().order_by("views")
   # queryset = VideoModel.objects.all().order_by("views")
    #queryset = randomvid
    serializer_class = VideoModelSerializer
    pagination_class = StandardResultsPagination


# class AllTimeGenreAPIView(generics.ListAPIView):
#     serializer_class = VideoModelSerializer
#     pagination_class = ChartResultsPagination
#     def get_queryset(self, *args, **kwargs):
#         genrename = GenreModel.objects.get(genrename__iexact=self.kwargs.get("genrename"))
#         qs = VideoModel.objects.filter(genre_id=genrename.pk).order_by("views")[:100]
#         return qs
# class AllTimeAPIView(generics.ListAPIView):
#
#     queryset = VideoModel.objects.all().order_by("views")[:100]
#     #queryset = VideoModel.objects.all().order_by("views")
#     #queryset = randomvid
#     serializer_class = VideoModelSerializer
#     pagination_class = StandardResultsPagination

    # def get_serializer_context(self, *args, **kwargs):
    #     context = super(TagVideoAPIView, self).get_serializer_context(*args, **kwargs)
    #     context['request'] = self.request
    #     return context
    #
    # def get_queryset(self, *args, **kwargs):
    #     hashtag = self.kwargs.get("hashtag")
    #     hashtag_obj = None
    #     try:
    #         hashtag_obj = HashTagModel.objects.get_or_create(tag=hashtag)[0]
    #     except:
    #         pass
    #     if hashtag_obj:
    #         qs = hashtag_obj.get_videos()
    #         query = self.request.GET.get("q", None)
    #         if query is not None:
    #             qs = qs.filter(
    #                     Q(description__icontains=query) |
    #                     Q(user__username__icontains=query)
    #                     )
    #         return qs
    #     return None