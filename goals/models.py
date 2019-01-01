from django.db import models


class Goal(models.Model):
    name = models.CharField(help_text="The name of the goal", max_length=255)
    description = models.TextField(help_text="The description of the goal")
    image = models.ImageField(
        help_text="An image for the goal", upload_to="goals")
    slug = models.SlugField(
        max_length=100, help_text="The text for this goal used in its URL")
    percentage_complete = models.PositiveIntegerField(
        help_text="The percentage of the goal complete")

    def __str__(self):
        return "Goal: {}".format(self.name)
