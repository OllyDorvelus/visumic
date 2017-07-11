from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response


from videos.models import VideoModel

from videos.api.pagination import StandardResultsPagination
from videos.api.serializers import VideoModelSerializer

from hashtags.models import HashTagModel

class TagVideoAPIView(generics.ListAPIView):
    queryset = VideoModel.objects.all().order_by("-timestamp")
    serializer_class = VideoModelSerializer
    pagination_class = StandardResultsPagination

    def get_serializer_context(self, *args, **kwargs):
        context = super(TagVideoAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self, *args, **kwargs):
        hashtag = self.kwargs.get("hashtag")
        hashtag_obj = None
        try:
            hashtag_obj = HashTagModel.objects.get_or_create(tag=hashtag)[0]
        except:
            pass
        if hashtag_obj:
            qs = hashtag_obj.get_videos()
            query = self.request.GET.get("q", None)
            if query is not None:
                qs = qs.filter(
                        Q(description__icontains=query) |
                        Q(user__username__icontains=query)
                        )
            return qs
        return None