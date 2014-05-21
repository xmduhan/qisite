# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *


class UserAdmin(admin.ModelAdmin):
    fields = [
        'code', 'phone', 'email', 'name', 'birthDate', 'createBy', 'modifyBy',
        'createTime', 'modifyTime'
    ]
    list_display = ['code','name','phone','email','createTime']


admin.site.register(User, UserAdmin)