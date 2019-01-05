from django.db import models


class Task(models.Model):
    goal = models.ForeignKey('Goal', on_delete=models.CASCADE)
    name = models.CharField(help_text="The name of the goal", max_length=255)
    url = models.URLField(help_text="The URL of this task")
    completed = models.BooleanField(help_text="Whether or not this task is complete",
                                    default=False)

    def complete(self):
        self.completed = True
        self.save()


class Goal(models.Model):
    name = models.CharField(help_text="The name of the goal", max_length=255)
    description = models.TextField(help_text="The description of the goal", blank=True, null=True)
    image = models.ImageField(
        help_text="An image for the goal", upload_to="goals")
    slug = models.SlugField(
        max_length=100, help_text="The text for this goal used in its URL")

    def __str__(self):
        return "Goal: {}".format(self.name)

    def percentage_complete(self):
        completed = self.task_set.filter(completed=True).count()
        if completed == 0:
            return 0
        return (completed / self.task_set.count()) * 100
