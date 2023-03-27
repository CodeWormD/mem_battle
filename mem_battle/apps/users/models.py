import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.cores.models import TimestampsBaseMixin


class Social(models.Model):
    class SocialNetworks:
        VK = 'VK'
        Telegram = 'Telegram'
        USER_SOCIALS =(
            (VK, 'VK'),
            (Telegram, 'Telegram')
        )

    name = models.CharField(
        choices=SocialNetworks.USER_SOCIALS,
        max_length=20,
        unique=True
    )
    link = models.URLField(
        max_length=355,
        unique=True
    )


class User(AbstractUser, TimestampsBaseMixin):
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True
    )
    username = models.TextField(
        verbose_name='User nickname',
        db_index=True,
        max_length=100,
        unique=True
    )
    email = models.EmailField(
        verbose_name='User email',
        db_index=True,
        max_length=254,
        unique=True
    )
    is_active = models.BooleanField(
        default=False
    )
    social = models.ForeignKey(
        Social,
        related_name='users',
        on_delete=models.CASCADE,
    )
    follower = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Follower',
        through_fields=('sender', 'receiver')
    )

    class Mets:
        db_table = 'User',
        verbose_name = 'User',
        verbose_name_plural ='Users',

    def __str__(self):
        return self.email


class Follower(models.Model):
    sender = models.ForeignKey(
        User,
        related_name='sender',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User,
        related_name='receiver',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.sender} подписался на {self.reciever}'


