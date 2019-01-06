from django.urls import path
from . import views

urlpatterns = [
    path('', views.goals_list),
    path('goal/<int:pk>/', views.goal_detail, name='goal_detail'),
]
