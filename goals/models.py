from django.db import models


class Goal(models.Model):
    title = models.TextField(help_text="The title of the goal")
    description = models.TextField(help_text="The description of the goal")
    image = models.ImageField(
        help_text="An image for the goal", upload_to="goals")
    slug = models.SlugField(
        max_length=100, help_text="The text for this goal used in its URL")

    def __str__(self):
        return "Goal: {}".format(self.title)
