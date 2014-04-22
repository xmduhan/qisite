# coding=utf-8
# Create your views here.



from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader
from qisite import settings
from django.db import models
from models import *

def getFieldNameList():
    result = []
    for i in dir(models) :
        if i[-5:] == 'Field' :
            result.append(i)
    return result

def test(request):
    result = u''
    for app in settings.INSTALLED_APPS:
        modelsFilePath = app + ".models"
        if modelsFilePath.split('.')[0] != 'django':
            modelsFile = __import__(modelsFilePath, fromlist=["models"])
            modelNames = dir(modelsFile)
            for modelName in modelNames:
                model = modelsFile.__getattribute__(modelName)
                if type(model).__module__== 'django.db.models.base':
                    result += u'%s.%s<br>' % (modelsFilePath, modelName)
                    fieldNames = model._meta.get_all_field_names()
                    fieldNameList = getFieldNameList()
                    for fieldName in fieldNames :
                        field = model._meta.get_field_by_name(fieldName)[0]
                        fieldType = field.__class__.__name__
                        #field = Catalog._meta.get_field_by_name('papers')[0]
                        #field.rel.to
                        result += u'&nbsp;&nbsp;%s,%s<br>' % (fieldName,fieldType)
    return HttpResponse(result)

def test01(request):
    template = loader.get_template('home/test01.html')
    context = Context({})
    return HttpResponse(template.render(context))

def test02(request):
    template = loader.get_template('home/test02.html')
    context = Context({})
    return HttpResponse(template.render(context))

def ajaxtest(request):
    template = loader.get_template('home/ajaxtest.html')
    context = Context({})
    return HttpResponse(template.render(context))


def test1(request):
    Catalog().__getattribute__('name')
    return HttpResponse('hello')



def index(request):
    template = loader.get_template('home/index.html')
    context = Context({})
    return HttpResponse(template.render(context))  # 调用index.html模板
