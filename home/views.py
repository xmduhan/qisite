# coding=utf-8
# Create your views here.



from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader
from qisite import settings
from django.db import models

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
        try:
            modelsFile = __import__(modelsFilePath, fromlist=["models"])
            modelNames = dir(modelsFile)
            for modelName in modelNames:
                try:
                    model = modelsFile.__getattribute__(modelName)
                    if issubclass(model, models.Model) and model.__module__ == modelsFilePath:
                        result += u'%s.%s<br>' % (modelsFilePath, modelName)
                        attrNames = dir(model)
                        fieldNameList = getFieldNameList()
                        for attrName in attrNames :
                            attr = model.__getattribute__(attrName)
                            if type(attr).__name__ in fieldNameList:
                                result += u'&nbsp;&nbsp;%s<br>' % attrName
                except TypeError, e:
                    print e
                    pass
        except ImportError, e:
            pass
    return HttpResponse(result)


def index(request):
    template = loader.get_template('home/index.html')
    context = Context({})
    return HttpResponse(template.render(context))  # 调用index.html模板
