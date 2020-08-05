from django.db import models
from django.contrib.auth.models import User

from quest.models import QuestModel


# tag::Account[]
class Account(QuestModel):
    name = models.CharField(max_length=255, help_text="Name of the account")
# end::Account[]


# tag::UserProfile[]
class UserProfile(QuestModel):
    user = models.OneToOneField(
        User,
        related_name='profile',
        help_text="The user to whom this profile belongs",
        on_delete=models.CASCADE)
    account = models.OneToOneField(  # <1>
        Account,
        help_text="The account to which this user belongs",
        on_delete=models.DO_NOTHING)
# end::UserProfile[]
