import uuid
from django.db import models
from django.conf import settings
# from django.urls import reverse
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify

from utils.mem_path_save import user_directory_path
from apps.cores.mixins import LikeDislikeTimeMixin


User = settings.AUTH_USER_MODEL



class Group(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True
    )
    name = models.CharField(
        max_length=70,
        unique=True,
        db_index=True
    )
    slug = models.SlugField(
        unique=True,
        max_length=70
    )
    owner = models.ForeignKey(
        User,
        related_name='group_owner',
        null=True,
        on_delete=models.SET_NULL
    )
    members = models.ManyToManyField(
        User,
        blank=True,
        related_name='group_members'
    )


    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    # def get_absolute_url(self):
        # return reverse("model_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Group, self).save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(
        max_length=70,
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        max_length=70
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.name:
            self.name = self.name.lower()
        super(Tag, self).save(*args, **kwargs)


class Mem(LikeDislikeTimeMixin):
    image = models.ImageField(
        'Изображение',
        upload_to=user_directory_path
    )
    owner = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='mems',
        null=True,
        on_delete=models.SET_NULL
    )
    vote_score = models.IntegerField(
        default=0
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='mems',
    )
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='mems_group'
    )

    class Meta:
        verbose_name = 'Мем'
        verbose_name_plural = 'Мемы'

    def __str__(self):
        return f'{self.id}'


class Comment(LikeDislikeTimeMixin):
    mem = models.ForeignKey(
        Mem,
        related_name='comments',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='threads'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.id}'