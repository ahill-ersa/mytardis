from django.conf.urls import patterns, include, url
from tardis.apps.acad import views

urlpatterns = patterns('',
    url(r'^source/$', views.source_index, name='source_index'),
    url(r'^source/(?P<id>\w+)/$', views.source_detail, name='source_detail'),
)
