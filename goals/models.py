from django.db import models


class Task(models.Model):
    goal = models.ForeignKey(
        'Goal', on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(help_text="The name of the goal", max_length=255)
    url = models.URLField(help_text="The URL of this task")

    def is_completed(self, user):
        return self.statuses.filter(user=user, status=TaskStatus.DONE).exists()

    def complete(self, user):
        completion = this.statuses.get_or_create(user=user)
        completion.update(status=TaskStatus.DONE)

    def __str__(self):
        return 'Task: {}'.format(self.name)


class TaskStatus(models.Model):
    INCOMPLETE = 1
    DONE = 2
    CHOICES = (
        (INCOMPLETE, 'Incomplete'),
        (DONE, 'Done'),
    )

    task = models.ForeignKey(
        'Task', on_delete=models.CASCADE, related_name='statuses')
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='task_statuses')
    status = models.PositiveSmallIntegerField(
        help_text="The status of this task", default=False, choices=CHOICES)

    def complete(self):
        self.status = DONE
        self.save()

    def status_text(self):
        if self.status == self.INCOMPLETE:
            return 'incomplete'
        return 'done'

    def __str__(self):
        return "{} {} by {}".format(self.task.name, self.status_text,
                                    self.user)

    class Meta:
        unique_together = ('user', 'task')


class Goal(models.Model):
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='goals')
    name = models.CharField(help_text="The name of the goal", max_length=255)
    description = models.TextField(
        help_text="The description of the goal", blank=True, null=True)
    image = models.ImageField(
        help_text="An image for the goal", upload_to="goals")
    slug = models.SlugField(
        max_length=100, help_text="The text for this goal used in its URL")
    is_public = models.BooleanField(
        default=False,
        help_text="Whether or not this goal is publicly accessible")

    def __str__(self):
        return self.name

    def percentage_complete(self, user):
        completed = self.tasks.filter(
            statuses__status=TaskStatus.DONE, user=user).count()
        if completed == 0:
            return 0
        return (completed / self.tasks.count()) * 100
