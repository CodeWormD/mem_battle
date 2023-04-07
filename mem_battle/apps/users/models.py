import uuid

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from apps.cores.mixins import TimestampsBaseMixin

User = settings.AUTH_USER_MODEL



class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user



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
    is_verified = models.BooleanField(
        default=False
    )
    follower = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Follower',
        through_fields=('sender', 'receiver')
    )

    objects = UserManager()

    class Mets:
        db_table = 'User',
        verbose_name = 'User',
        verbose_name_plural ='Users',

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)



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


