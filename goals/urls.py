from django.urls import path

from . import views

urlpatterns = [
    path('api/goal/', views.GoalListCreate.as_view(), name='list_goals'),
]
