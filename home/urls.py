from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^test$', views.test, name='test'),
    url(r'^test01$', views.test01, name='test01'),
    url(r'^test02$', views.test02, name='test02'),
    url(r'^ajaxtest$', views.ajaxtest, name='ajaxtest'),
    url(r'^$', views.index, name='index')
)