__author__ = 'OllyD'

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^events/(?P<pk>\d+)/$', views.EventDetailView.as_view(), name='event_detail'),
    url(r'^events/update/(?P<pk>\d+)/$', views.EventUpdateView.as_view(), name='event_update'),
    url(r'^events/$', views.EventListView.as_view(), name='event_list'),
    url(r'^events/create/$', views.EventCreateView.as_view(), name='event_create')

]