__author__ = 'OllyD'
from django.conf.urls import url
from . import views

app_name = 'charts'


urlpatterns = [
    url(r'^Vcharts/(?P<category>[\w.@+-]+)/$', views.ChartView.as_view(), name="chart_list"),
    url(r'^Vcharts/(?P<category>[\w.@+-]+)/alltime/$', views.ChartViewAllTime.as_view(), name="chart_list_alltime"),
    url(r'^Vcharts/daily/$', views.ChartViewDaily, name="chart_list_daily"),
   # url(r'^Vcharts/alltime/(?P<genrename>[\w.@+-]+)/$', views.ChartViewAllTimeGenre.as_view(), name='alltime_genre'),


]