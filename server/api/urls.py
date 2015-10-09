from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    # url(r'^importdata/(?P<admin_id>\w*)', views.import_data),
    url(r'^importdata/', views.ImportData.as_view())
    # url(r'^getdata/', views.get_data)
]
