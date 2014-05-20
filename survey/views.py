# Create your views here.

from django.http import HttpResponse
from django.template import Context,loader



def surveyEdit(request):
    template = loader.get_template('survey/SurveyEdit.html')
    context = Context({})
    return HttpResponse(template.render(context))