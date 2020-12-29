from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Q
from quest.models import QuestModel


# tag::Event[]
class Event(QuestModel):
    name = models.CharField(help_text="The name of the event", max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             help_text="The user associated with this event",
                             on_delete=models.CASCADE, related_name="events",
                             null=True, blank=True)
    data = JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['name'], name="analytics_event_name_idx",
                         condition=Q(name="goal_viewed")),
        ]
# end::Event[]
