from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^loguot$', views.logout, name='logout'),
    url(r'^recovery$', views.recovery, name='recovery'),
)