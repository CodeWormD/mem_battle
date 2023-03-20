from django.contrib.auth.models import AbstractUser, Group
from django.db import models



class User(AbstractUser):

    username = models.TextField(
        verbose_name='User nickname',
        blank=True,
        null=True,
        unique=True
    )
    email = models.EmailField(
        verbose_name='User email',
        unique=True,
    )
