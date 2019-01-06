from rest_framework import serializers
from goals.models import Goal, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('name', 'completed')


class GoalSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=False)

    class Meta:
        model = Goal
        fields = ('id', 'name', 'description', 'slug', 'percentage_complete',
                  'tasks')
