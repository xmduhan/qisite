from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',

    url(r'^test$', views.test, name='test'),
    url(r'^$', views.index, name='index')
)