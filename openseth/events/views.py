from django.core.serializers import serialize
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Event

def index(request):
    data = serialize("json", Event.objects.all())
    return HttpResponse(data, content_type="application/json")

