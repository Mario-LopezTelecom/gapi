from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'calendars', views.CalendarViewSet, base_name="calendars")

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'oauth2callback', views.auth_return, name='return'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]