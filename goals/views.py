from rest_framework import generics, status
from rest_framework.response import Response

from analytics.models import Event
from goals.models import Goal, Task, TaskStatus
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

    def perform_create(self, serializer):
        serializer.save()
        Event.objects.create(name="task_created", data=serializer.data,
                             user=self.request.user)


class TaskView(UserOwnedTaskMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateTaskSerializer
        return TaskSerializer


class GoalListCreateView(UserOwnedGoalMixin, generics.ListCreateAPIView):
    def perform_create(self, serializer):
        goal = serializer.save()
        Event.objects.create(name="goal_created", user=goal.user,
                             data=serializer.data)

    def get(self, request, *args, **kwargs):
        Event.objects.create(name="goal_list_viewed", user=request.user,
                             data={})
        return self.list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewGoalSerializer
        return GoalSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Goal.objects.all()
        is_public = self.request.query_params.get('is_public', None)
        has_started = self.request.query_params.get('has_started', None)

        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
            if is_public is not None:
                queryset = queryset.filter(is_public=is_public == 'true')
        else:
            queryset = queryset.filter(is_public=True)

        if has_started is not None:
            if has_started == 'true':
                queryset = queryset.filter(
                    tasks__statuses__status=TaskStatus.DONE) | queryset.filter(
                    tasks__statuses__status=TaskStatus.STARTED)
            else:
                queryset = queryset.exclude(
                    tasks__statuses__status=TaskStatus.DONE).exclude(
                    tasks__statuses__status=TaskStatus.STARTED)

        return queryset


# tag::goal-view-a[]
class GoalView(UserOwnedGoalMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer  # <1>

    # end::goal-view-a[]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        Event.objects.create(name="goal_viewed", data={"goal_id": instance.id},
                             user=request.user)
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return NewGoalSerializer
        return GoalSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_public:
            instance.clear_status_for_user(self.request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return self.destroy(request, *args, **kwargs)


class GoalStartView(UserOwnedGoalMixin, generics.GenericAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

    def post(self, request, pk, *args, **kwargs):
        goal = self.get_object()
        goal.start(self.request.user)
        serializer = self.get_serializer(goal)
        return Response(serializer.data)
