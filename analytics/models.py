from django.contrib.postgres.fields import JSONField
from django.db import models


# tag::Event[]
class Event(models.Model):
    name = models.CharField(help_text="The name of the event", max_length=255)
    data = JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['name']), # <1>
        ]
# end::Event[]
