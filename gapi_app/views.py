from django.shortcuts import render
from django.http import HttpResponse
from services import gcal_api_example

def index(request):
    return HttpResponse(gcal_api_example())
    #return HttpResponse(gcal_api_example())

# Create your views here.
