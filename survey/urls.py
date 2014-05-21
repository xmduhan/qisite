from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^survey$', views.surveyList, name='survey'),
    url(r'^paper$', views.paperList, name='paper'),
    url(r'^list$', views.custListList, name='list'),
)