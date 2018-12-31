from rest_framework import serializers
from goals.models import Goal

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('id', 'name', 'description', 'slug')
