# coding=utf-8
from django.conf.urls import patterns, url, include


from views import router

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)