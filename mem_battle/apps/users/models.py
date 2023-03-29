import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from apps.cores.mixins import TimestampsBaseMixin


User = settings.AUTH_USER_MODEL


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

    # def get_absolute_url(self):
        # return reverse("model_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.username


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
    user = models.ForeignKey(
        User,
        related_name='socials',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    link = models.URLField(
        max_length=355,
        unique=True
    )

    class Mets:
        verbose_name = 'Социальная сеть',
        verbose_name_plural ='Социальные сети',

    def __str__(self):
        return f'{self.user} добавил социальную сеть {self.name}'


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

    class Mets:
        verbose_name = 'Подписчик',
        verbose_name_plural ='Подписчики',

    def __str__(self):
        return f'{self.sender} подписался на {self.reciever}'


