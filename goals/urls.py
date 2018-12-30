from django.urls import path

from . import views

urlpatterns = [
    path('', views.GoalList.as_view(), name='list_goals'),
    path('create', views.GoalCreate.as_view(), name='create_goal'),
]
