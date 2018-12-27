from django.urls import path

from . import views

urlpatterns = [
    path('', views.GoalList.as_view(), name='index'),
]
