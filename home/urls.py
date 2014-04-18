from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',

    url(r'^test$', views.test, name='test'),
    url(r'^ajaxtest$', views.ajaxtest, name='ajaxtest'),
    url(r'^$', views.index, name='index')
)