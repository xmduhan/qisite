# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *


class UserAdmin(admin.ModelAdmin):
    fields = [
        'code', 'phone', 'email', 'name', 'birthDate', 'createBy', 'modifyBy',
        'createTime', 'modifyTime'
    ]
    list_display = ['code', 'name', 'phone', 'email', 'createTime']


admin.site.register(User, UserAdmin)


class SmsCheckCodeAdmin(admin.ModelAdmin):
    fields = [
        'phone', 'checkCode', 'createTime'
    ]
    list_display = ['phone', 'checkCode', 'createTime']


admin.site.register(SmsCheckCode, SmsCheckCodeAdmin)