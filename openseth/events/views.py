from django.core.serializers import serialize
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Event

def get_events(request):
    if request.method != 'GET':
        return
    
    data = serialize("json", Event.objects.all())
    response = HttpResponse(data, content_type="application/json")
    response.set_cookie('csrftoken', csrf.get_token(request))
    
    return response


def manage_events(request):
    print("york")
    if request.method != 'POST':
        return HttpResponse('200')
    
    print('Post: "{}"'.format(request.POST))
    print('Body: "{}"'.format(request.body))
    
    return HttpResponse('200')
    
