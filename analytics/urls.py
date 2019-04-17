from django.urls import path
from . import views

urlpatterns = [
    path('analytics', views.events),
]
