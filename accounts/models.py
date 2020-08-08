from django.db import models
from django.contrib.auth.models import User

from quest.models import QuestModel


class Account(QuestModel):
    name = models.CharField(max_length=255, help_text="Name of the account")


class UserProfile(QuestModel):
    user = models.OneToOneField(
        User,
        related_name='profile',
        help_text="The user to whom this profile belongs",
        on_delete=models.CASCADE)
    account = models.OneToOneField(
        Account,
        help_text="The account to which this user belongs",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True)
