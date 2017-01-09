from django.shortcuts import render
from django.http import HttpResponse
from services import gcal_api_example
from services import auth_return_service

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return gcal_api_example(request)

@login_required
def auth_return(request):
    return auth_return_service(request)

