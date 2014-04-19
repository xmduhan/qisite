# coding=utf-8
# Create your views here.

from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from rest_framework import routers
from rest_framework.viewsets import ModelViewSet
import home


def prferMedia(http_accept):
    return http_accept.split(',')[0]

def isJsonMedia(request):
    http_accept = request.META['HTTP_ACCEPT']
    if prferMedia(http_accept) in ['application/json'] : # ,'text/html']:
        return True
    else:
        return False

# 重载ModelViewSet屏蔽json以外的访问方式
class JsonModelViewSet(ModelViewSet):
    errorResponse = HttpResponse("{'status': 'only json accept'}")
    #def __init__(self,**kwargs):
    #    return super(ModelViewSet, self).__init__(**kwargs)

    def list(self, request):
        if (isJsonMedia(request)):
            return super(ModelViewSet, self).list(request)
        else:
            return self.errorResponse

    def create(self, request):
        if (isJsonMedia(request)):
            return super(ModelViewSet, self).create(request)
        else:
            return self.errorResponse

    def retrieve(self, request, pk=None):
        if (isJsonMedia(request)):
            return super(ModelViewSet, self).retrieve(request, pk)
        else:
            return self.errorResponse

    def update(self, request, pk=None):
        if (isJsonMedia(request)):
            return super(ModelViewSet, self).update(request, pk)
        else:
            return self.errorResponse

    def partial_update(self, request, pk=None):
        if (isJsonMedia(request)):
            return super(ModelViewSet, self).partial_update(request, pk)
        else:
            return self.errorResponse

    def destroy(self, request, pk=None):
        if (isJsonMedia(request)):
            return super(ModelViewSet, self).destroy(request, pk)
        else:
            return self.errorResponse


# ViewSets define the view behavior.
class UserViewSet(JsonModelViewSet):
    model = User


class GroupViewSet(ModelViewSet):
    model = Group


class CatalogViewSet(ModelViewSet):
    model = home.models.Catalog

# Routers provide an easy way of automatically determining the URL conf.

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'catalog', CatalogViewSet)
