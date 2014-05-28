from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^survey/list$', views.surveyList, name='surveyList'),
    url(r'^survey/edit$', views.surveyEdit, name='surveyEdit'),
    url(r'^paper/list$', views.paperList, name='paperList'),
    url(r'^paper/edit/(?P<paperId>\d+)$', views.paperEdit, name='paperEdit'),
    url(r'^custlist/list$', views.custListList, name='custlistList'),
)