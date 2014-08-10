from django.conf.urls import patterns, url
import views
import services

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='home'),
    url(r'^index$', views.index, name='index'),
    url(r'^help$', views.help, name='help'),
    url(r'^dialog/confirmDialog$', views.confirmDialog, name='view.dailog.confirmDialog'),
    url(r'^dialog/messageDialog$', views.messageDialog, name='view.dialog.messageDialog'),
    url(r'^django/reverse$', services.djangoReverse, name='service.django.reverse'),
)