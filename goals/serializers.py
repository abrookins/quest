from rest_framework import serializers
from goals.models import Goal, Task


class TaskSerializer(serializers.ModelSerializer):
    goal = serializers.PrimaryKeyRelatedField(queryset=Goal.objects.all())

    class Meta:
        model = Task
        fields = ('id', 'name', 'completed', 'goal')


class NewGoalSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = ('id', 'user', 'name', 'description', 'slug',
                  'percentage_complete')


class GoalSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=False)

    class Meta:
        model = Goal
        fields = ('id', 'name', 'description', 'slug', 'percentage_complete',
                  'tasks')
