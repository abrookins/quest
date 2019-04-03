from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    users = models.OneToOne(User, related_name)
