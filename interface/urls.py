#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import wechat


urlpatterns = patterns(
    '',
    # 列表页面
    url(r'^wechat$', wechat.service, name='wechat'),

)