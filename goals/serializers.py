from rest_framework import serializers
from goals.models import Goal, Task, TaskStatus


class NewTaskSerializer(serializers.ModelSerializer):
    goal = serializers.PrimaryKeyRelatedField(queryset=Goal.objects.all())

    class Meta:
        model = Task
        fields = ('id', 'name', 'goal')


class UpdateTaskSerializer(serializers.ModelSerializer):
    goal = serializers.PrimaryKeyRelatedField(queryset=Goal.objects.all())
    completed = serializers.BooleanField(write_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'goal', 'completed')

    def update(self, instance, validated_data):
        # TODO: This should be somewhere else - maybe a service object.
        completed = validated_data.pop('completed')
        task = super().update(instance, validated_data)
        status = TaskStatus.DONE if completed else TaskStatus.INCOMPLETE
        task_status, _ = task.statuses.get_or_create(
            user=self.context['request'].user)
        task_status.status = status
        task_status.save()
        return instance


class TaskSerializer(serializers.ModelSerializer):
    goal = serializers.PrimaryKeyRelatedField(queryset=Goal.objects.all())
    completed = serializers.SerializerMethodField('is_completed')

    class Meta:
        model = Task
        fields = ('id', 'name', 'goal', 'completed')

    def is_completed(self, task):
        return task.statuses.filter(
            user=self.context['request'].user,
            task=task,
            status=TaskStatus.DONE).exists()


class NewGoalSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = ('id', 'user', 'name')


class GoalSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)
    percentage_complete = serializers.SerializerMethodField(
        'calc_percentage_complete')
    user_has_started = serializers.SerializerMethodField('has_started')

    class Meta:
        model = Goal
        fields = ('id', 'name', 'description', 'slug', 'tasks',
                  'percentage_complete', 'user_has_started', 'is_public')

    def calc_percentage_complete(self, goal):
        return goal.percentage_complete(self.context['request'].user)

    def has_started(self, goal):
        return goal.has_started(self.context['request'].user)
