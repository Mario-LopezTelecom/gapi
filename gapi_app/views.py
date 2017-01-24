from __future__ import print_function
import httplib2
import datetime

from apiclient import discovery
from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_orm import Storage
from gapi_app.models import CredentialsModel, FlowModel
from gapi import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    FLOW = settings.FLOW
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        f = FlowModel(id=request.user, flow=FLOW)
        f.save()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        res = 'Getting the upcoming 10 events'
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            res += 'No upcoming events found.'
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            res += start + event['summary']
        return HttpResponse(res)

@login_required
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

