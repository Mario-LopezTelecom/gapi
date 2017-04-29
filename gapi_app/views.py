from __future__ import print_function
import httplib2
import datetime

from apiclient import discovery
from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_orm import Storage
from gapi_app.models import CredentialsModel, FlowModel, Calendar, CalendarEvent
from gapi import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from rest_framework import mixins
from rest_framework import viewsets
from serializers import *

@login_required
def index(request):
    FLOW = settings.FLOW
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        f = FlowModel(id=request.user, flow=FLOW)
        f.save()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = discovery.build('calendar', 'v3', http=http)
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        page_token = None
        calendar_ids = []
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar in calendar_list['items']:
                cal_id = Calendar.objects.get_or_create(id=calendar['id'], name=calendar['summary'], user=request.user)
                calendar_ids.append(calendar['id'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        res = 'Getting the upcoming 10 events of first calendar'
        eventsResult = service.events().list(calendarId=calendar_ids[0], timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        if not events:
            res += 'No upcoming events found.'
        for event in events:
            if 'dateTime' in event['start']:
                CalendarEvent.objects.get_or_create(id=event['id'],
                                                    calendar_id=calendar_ids[0],
                                                    description=event['summary'],
                                                    date_start=event['start']['dateTime'],
                                                    date_end=event['end']['dateTime'])
                start = event['start'].get('dateTime', event['start'].get('date'))
                res += start + event['summary']
        return HttpResponse(res)

def auth_return(request):
    user = request.user
    FLOW = FlowModel.objects.get(id=user).flow
    if not xsrfutil.validate_token(
            FLOW.client_secret, str(request.GET['state']), user):
        return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.GET)
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/gapi")


class CalendarViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = CalendarSerializer

    def get_queryset(self):
        request_user = self.request.user
        return Calendar.objects.filter(user=request_user)
