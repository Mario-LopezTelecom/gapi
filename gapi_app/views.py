from django.shortcuts import render
from django.http import HttpResponse
from services import gcal_api_example
from services import auth_return_service

def index(request):
    return HttpResponse(gcal_api_example(request))

def auth_return(request):
    return HttpResponse(auth_return_service(request))

