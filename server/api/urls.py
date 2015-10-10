from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^freeroomat/(?P<time>\w+)', views.FindFreeRoomAt.as_view()),
    url(r'^importdata/', views.ImportData.as_view())
]
