import uuid
import random
# from numpy import random
from django.conf import settings
from django.db import models
from django.db.models.aggregates import Count
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
# from django.urls import reverse
from django.utils.text import slugify

from apps.cores.mixins import LikeDislikeTimeMixin
from utils.mem_path_save import user_directory_path

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

    def __str__(self):
        return self.name

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


class MemBattleManager(models.Manager):

    def random(self):
        count = self.values_list('id', flat=True)
        rand = random.choices(count, k=2)
        print(rand)
        return self.select_related('owner').filter(pk__in=rand)


class Mem(LikeDislikeTimeMixin):
    objects = MemBattleManager()
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
    vote_score = models.PositiveIntegerField(
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
        # ordering = ('tags',)

    def __str__(self):
        return f'{self.id}'

    def count_likes(self):
        return self.likes.count()


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
        on_delete=models.SET_NULL, # comment should stay in thread
        related_name='threads'
    )
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.id}'

    def children(self):
        return Comment.objects.filter(parent=self)