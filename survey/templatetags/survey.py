# -*- coding:utf-8 -*-

from django import template
import json

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def toJsonString(obj):
    return json.dumps(obj)
