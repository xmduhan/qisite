from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^register$', views.register, name='register'),
)