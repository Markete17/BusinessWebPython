from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.services_list, name = 'services')
]
