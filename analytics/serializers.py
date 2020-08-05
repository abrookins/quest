from rest_framework import serializers

from analytics.models import Event


class EventSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = Event
        fields = ('id', 'name', 'user', 'data')

