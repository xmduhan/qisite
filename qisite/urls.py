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
    url(r'^account/', include('account.urls', namespace="account")),
    url(r'^interface/', include('interface.urls', namespace="interface")),
    url(r'^demos/', include('demos.urls', namespace="demos")),
    url(r'^home/', include('home.urls', namespace="home")),
    #url(r'^restful/', include('restful.urls', namespace="restful")),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
