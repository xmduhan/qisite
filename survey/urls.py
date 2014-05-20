from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^survey/edit$', views.surveyEdit, name='SurveyEdit'),
)