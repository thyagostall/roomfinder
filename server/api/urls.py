from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^findroomat/(?P<schedule>\w*)', views.find_room_at),
    url(r'^importdata/(?P<admin_id>\w*)', views.import_data)
]
