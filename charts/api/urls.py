__author__ = 'OllyD'
from . import views
from django.conf.urls import url


urlpatterns = [
           url(r'^(?P<category>[\w.@+-]+)/alltime/$', views.AllTimeAPIView.as_view(), name="chartapi_list"),
           url(r'^daily/$', views.DailyAPIView.as_view(), name="chartapi_dailylist"),
          # url(r'^alltime/(?P<genrename>[\w.@+-]+)/$', views.AllTimeGenreAPIView.as_view(), name='alltimegenre'),

        ]