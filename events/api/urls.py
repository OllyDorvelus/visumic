__author__ = 'OllyD'
app_name = "eventsapi"
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.EventAPIListView.as_view(), name='event_list_api'),
    url(r'^(?P<pk>\d+)/$', views.EventAPIDetailView.as_view(), name='event_detail_api'),
    url(r'^(?P<pk>\d+)/attend/$', views.AttendToggle.as_view(), name='event_toggle_api'),



]