from django.db import models
from django.contrib.auth.models import User


# tag::Account[]
class Account(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the account")
# end::Account[]


# tag::UserProfile[]
class UserProfile(models.Model):
    user = models.ForeignKey(
        User,
        help_text="The user to whom this profile belongs",
        on_delete=models.CASCADE)
    account = models.ForeignKey(  # <1>
        Account,
        help_text="The account to which this user belongs",
        on_delete=models.DO_NOTHING)
# end::UserProfile[]
