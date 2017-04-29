from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from oauth2client.contrib.django_orm import CredentialsField, FlowField


# OAuth related models
class FlowModel(models.Model):
    id = models.OneToOneField(User, primary_key=True)
    flow = FlowField()


class CredentialsModel(models.Model):
    id = models.OneToOneField(User, primary_key=True)
    credential = CredentialsField()


# gapi models
class Calendar(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)

class CalendarEvent(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    calendar = models.ForeignKey(Calendar, related_name="calendar_event")
    description = models.CharField(max_length=100, blank=True, default='')
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    @property
    def duration(self):
        return self.date_end - self.date_start

