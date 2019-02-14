from django.contrib.postgres.fields import JSONField
from django.db import models


class Event(models.Model):
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='events')
    name = models.CharField(help_text="The name of the event", max_length=255)
    data = JSONField()
