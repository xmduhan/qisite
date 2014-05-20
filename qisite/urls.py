from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('www.urls', namespace="home")),
    url(r'^www/', include('www.urls', namespace="www")),
    url(r'^survey/', include('survey.urls', namespace="survey")),
    url(r'^demos/', include('demos.urls', namespace="demos")),
    url(r'^restful/', include('restful.urls', namespace="restful")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
