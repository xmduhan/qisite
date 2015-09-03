from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^demo01$', views.demo01, name='demo01'),
    url(r'^demo02$', views.demo02, name='demo02'),
    url(r'^demo03$', views.demo03, name='demo03'),
    url(r'^demo04$', views.demo04, name='demo04'),
    url(r'^demo05$', views.demo05, name='demo05'),
    url(r'^demo06$', views.demo06, name='demo06'),
    url(r'^demo07$', views.demo07, name='demo07'),
    url(r'^demo08$', views.demo08.as_view(), name='demo07'),
    url(r'^demo09$', views.demo09, name='demo09'),
)
