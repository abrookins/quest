from rest_framework import generics
from goals.models import Goal, Task
from goals.serializers import (GoalSerializer, NewGoalSerializer,
                               TaskSerializer, NewTaskSerializer,
                               UpdateTaskSerializer)


class UserOwnedGoalMixin:
    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(
            user=self.request.user) | self.queryset.filter(is_public=True)


class UserOwnedTaskMixin:
    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(
            goal__user=self.request.user) | self.queryset.filter(
                goal__is_public=True)


class TaskListCreateView(UserOwnedTaskMixin, generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = NewTaskSerializer


class TaskView(UserOwnedTaskMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_update(self, serializer):
        task = serializer.save()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateTaskSerializer
        return TaskSerializer



class GoalListCreateView(UserOwnedGoalMixin, generics.ListCreateAPIView):
    queryset = Goal.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewGoalSerializer
        return GoalSerializer


class GoalView(UserOwnedGoalMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

    def get_serializer_context(self):
        return {'request': self.request}
