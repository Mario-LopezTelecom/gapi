from datetime import date
from rest_framework import serializers
from models import Calendar, CalendarEvent


class CalendarSerializer(serializers.ModelSerializer):
    total_time_for_period = serializers.SerializerMethodField()
    def get_total_time_for_period(self, obj):
        request = self.context.get("request")
        period_date_start = self.parse_date(request.query_params['period_date_start'])
        period_date_end = self.parse_date(request.query_params['period_date_end'])
        total_time_res = 0
        for event in obj.calendar_event.all():
            #TODO: what if event.date_start + duration goes beyond period_date_end
            if period_date_start < event.date_start.date() < period_date_end:
                total_time_res += event.duration.total_seconds()
        return total_time_res

    @staticmethod
    def parse_date(date_query_param):
        return date(*[int(date_elem) for date_elem in date_query_param.split("-")])


    class Meta:
        model = Calendar
        fields = ('name', 'total_time_for_period')
