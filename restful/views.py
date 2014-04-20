# coding=utf-8
# Create your views here.

from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import routers
from rest_framework.viewsets import ModelViewSet
from rest_framework import status


def prferMedia(http_accept):
    return http_accept.split(',')[0]


def isJsonMedia(request):
    http_accept = request.META['HTTP_ACCEPT']
    if prferMedia(http_accept) in ['application/json']:
    #if prferMedia(http_accept) in ['application/json','text/html']:
        return True
    else:
        return False


# 重载ModelViewSet屏蔽json以外的访问方式
class QiModelViewSet(ModelViewSet):

    def __init__(self,**kwargs):
        self.errorResponse = HttpResponse("{'status': 'only json accept'}")
        super(ModelViewSet, self).__init__(**kwargs)

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


# 定义需要提供restful服务的数据模型的代理类
class UserViewSet(QiModelViewSet):
    model = User


# 设置restful的url和代理类的关系
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
