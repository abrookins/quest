from django.urls import path

from . import views

urlpatterns = [
    path('api/goal/', views.GoalListCreateView.as_view(), name='list_goals'),
    path('api/goal/<int:pk>/', views.GoalView.as_view(), name='goal'),
    path(
        'api/goal/<int:pk>/start/',
        views.GoalStartView.as_view(),
        name='start_goal'),
    path('api/task/', views.TaskListCreateView.as_view(), name='list_tasks'),
    path('api/task/<str:uuid>/', views.TaskView.as_view(), name='task'),
]
