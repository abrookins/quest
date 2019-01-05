from django.urls import path

from . import views

urlpatterns = [
    path('api/goal/', views.GoalListCreateView.as_view(), name='list_goals'),
    path('api/goal/<int:pk>/', views.GoalView.as_view(), name='goal'),
]
