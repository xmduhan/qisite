# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *


class PaperAdmin(admin.ModelAdmin):
    fields = [
        'title', 'description', 'inOrder', 'questionNumStyle', 'lookBack', 'paging',
        'createBy', 'modifyBy', 'createTime', 'modifyTime'
    ]
    list_display = ('title', 'description', 'inOrder', 'lookBack', 'createBy', 'createTime')


admin.site.register(Paper, PaperAdmin)


class PaperCatalogAdmin(admin.ModelAdmin):
    fields = [
        'name', 'code', 'parent', 'ord', 'createBy', 'modifyBy', 'createTime', 'modifyTime'
    ]


admin.site.register(PaperCatalog, PaperCatalogAdmin)


class PaperCatalogPaperAdmin(admin.ModelAdmin):
    fields = [
        'paperCatalog', 'paper', 'ord', 'createBy', 'modifyBy', 'createTime', 'modifyTime'
    ]


admin.site.register(PaperCatalogPaper, PaperCatalogPaperAdmin)


class QuestionAdmin(admin.ModelAdmin):
    fields = [
        'type', 'ord', 'contentLength', 'valueMin', 'valueMax', 'confused', 'branchNumStyle',
        'nextQuestion', 'paper', 'createBy', 'modifyBy', 'createTime', 'modifyTime'
    ]
    list_display = ('ord', 'getStemText', 'type', 'branchNumStyle', 'paper', 'createBy', 'createTime')
    list_filter = ('paper',)


admin.site.register(Question, QuestionAdmin)


class QuestionCatalogAdmin(admin.ModelAdmin):
    fields = [
        'name', 'code', 'parent', 'ord', 'createBy', 'modifyBy', 'createTime', 'modifyTime'
    ]


admin.site.register(QuestionCatalog, QuestionCatalogAdmin)


class QuestionCatalogQuestionAdmin(admin.ModelAdmin):
    fields = [
        'questionCatalog', 'question', 'ord', 'createBy', 'modifyBy', 'createTime', 'modifyTime'
    ]


admin.site.register(QuestionCatalogQuestion, QuestionCatalogQuestionAdmin)


class ResourceAdmin(admin.ModelAdmin):
    fields = [
        'resourceType', 'resourceUrl', 'width', 'height', 'question', 'createBy', 'modifyBy',
        'createTime', 'modifyTime'
    ]


admin.site.register(Resource, ResourceAdmin)


class BranchAdmin(admin.ModelAdmin):
    fields = [
        'ord', 'text', 'question', 'nextQuestion', 'createBy', 'modifyBy', 'createTime', 'modifyTime'
    ]
    list_display = ('ord', 'question', 'text', 'nextQuestion', 'createBy', 'createTime')


admin.site.register(Branch, BranchAdmin)


class SurveyAdmin(admin.ModelAdmin):
    fields = [
        'paper', 'targetOnly', 'state', 'shared', 'viewResult', 'resubmit', 'password', 'ipLimit',
        'macLimit', 'publishTime', 'endTime', 'hardCost', 'bonus', 'fee', 'validSampleLimit',
        'createBy', 'modifyBy', 'createTime', 'modifyTime'
    ]
    list_display = ['paper', 'targetOnly', 'state', 'viewResult', 'createBy', 'createTime']


admin.site.register(Survey, SurveyAdmin)


class TargetCustAdmin(admin.ModelAdmin):
    fields = [
        'name', 'phone', 'email', 'defineInfo_set', 'token', 'survey', 'createBy', 'modifyBy',
        'createTime', 'modifyTime'
    ]


admin.site.register(TargetCust, TargetCustAdmin)


class SampleAdmin(admin.ModelAdmin):
    fields = [
        'targetCust', 'user', 'ipAddress', 'macAddress', 'finished', 'isValid', 'paper',
        'createBy', 'modifyBy', 'createTime', 'modifyTime'
    ]


admin.site.register(Sample, SampleAdmin)


class SampleItemAdmin(admin.ModelAdmin):
    fields = [
        'question', 'branch_set', 'content', 'score', 'sample', 'createBy', 'modifyBy',
        'createTime', 'modifyTime'
    ]


admin.site.register(SampleItem, SampleItemAdmin)


class CustListAdmin(admin.ModelAdmin):
    fields = [
        'name', 'descrition', 'createBy', 'modifyBy', 'createTime', 'modifyTime'
    ]
    list_display = ('name', 'descrition', 'createBy', 'createTime')


admin.site.register(CustList, CustListAdmin)


class CustListItemAdmin(admin.ModelAdmin):
    fields = [
        'name', 'phone', 'email', 'custList', 'defineInfo_set', 'createBy', 'modifyBy',
        'createTime', 'modifyTime'
    ]


admin.site.register(CustListItem, CustListItemAdmin)


class DefineInfoAdmin(admin.ModelAdmin):
    fields = [
        'name', 'value', 'ord', 'createBy', 'modifyBy', 'createTime', 'modifyTime'
    ]


admin.site.register(DefineInfo, DefineInfoAdmin)