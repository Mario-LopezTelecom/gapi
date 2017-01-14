from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from oauth2client.contrib.django_orm import CredentialsField, FlowField


class FlowModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    flow = FlowField()


class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()


class Calendar(models.Model):
    name = models.CharField(max_length=100)


class CalendarEvent(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    calendar_id = models.ForeignKey(Calendar)
    description = models.CharField(max_length=100, blank=True, default='')
    date_start = models.DateTimeField()


class PieSector(models.Model):
    calendar_id = models.ForeignKey(Calendar)
    diagram_id = models.ForeignKey(PieDiagram)
    size = models.FloatField()


class PieDiagram(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()






