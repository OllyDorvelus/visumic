__author__ = 'OllyD'
from rest_framework import generics, permissions, mixins
from videos.api.permissions import MyUserPermissions
from .serializers import EventModelSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from accounts.api.pagination import StandardResultsPagination
from accounts.models import UserProfile
from videos.api.serializers import VideoModelSerializer, ShareModelSerializer
from videos.models import VideoModel
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django_filters.rest_framework import DjangoFilterBackend
from events.models import EventModel

class EventAPIListView(generics.ListAPIView):
    serializer_class = EventModelSerializer
    pagination_class = StandardResultsPagination
   # filter_backends = [OrderingFilter]
    #ordering_fields = ('user__username','timestamp')
    def get_queryset(self, *args, **kwargs):
        qs = EventModel.objects.all().order_by("name")
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(description__icontains=query) |
                Q(name__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs

    def get_seralizer_context(self, *args, **kwargs):
        context = super(EventAPIListView, self).get_seralizer_context(*args, **kwargs)
        context['request'] = self.request
        return context

class EventAPIDetailView(generics.RetrieveAPIView, mixins.DestroyModelMixin):
    serializer_class = EventModelSerializer
    permission_classes = [MyUserPermissions]
    def get_queryset(self, *args, **kwargs):
        qs = EventModel.objects.all()
        return qs

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class AttendToggle(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, format=None):
        event_qs = EventModel.objects.filter(pk=pk)
        message = "Not allowed"
        if request.user.is_authenticated():
            is_attending = EventModel.objects.attend_toggle(request.user, event_qs.first())
            attending_count = EventModel.objects.attending_count(event_qs.first())
            return Response({"attending": is_attending, 'attending_count': attending_count})
        return Response({"message": message}, status=400)