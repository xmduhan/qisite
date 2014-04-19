from django.conf.urls import patterns, include, url
from django.contrib import admin



admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qisite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('home.urls',namespace="home")),
    url(r'^home/', include('home.urls',namespace="home")),
    url(r'^restful/', include('restful.urls',namespace="restful")),
)
