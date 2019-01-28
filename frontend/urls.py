from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('goals', views.goals_list),
    path('goal/new/', views.new_goal, name='new_goal'),
    path('goal/<int:pk>/', views.goal_detail, name='goal_detail'),
]
