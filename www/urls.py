from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='home'),
    url(r'^index$', views.index, name='index'),
    url(r'^help$', views.help, name='help'),
    url(r'^dialog/confirmDialog$', views.confirmDialog, name='confirmDialog'),
    url(r'^dialog/messageDialog$', views.messageDialog, name='messageDialog'),
)