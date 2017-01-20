from rest_framework import serializers
from gapi_app.models import CalendarEvent


class CalendarEventSerializer(serializers.ModelSerializer):
    calendar_id = serializers.StringRelatedField
    class Meta:
        model = CalendarEvent
        fields = ('calendar_id', 'description', 'date_start', 'date_end')

