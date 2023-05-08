import uuid

from django.conf import settings
from django.db import models

from rest_framework import viewsets, mixins


User = settings.AUTH_USER_MODEL


class TimestampsBaseMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ['-created_at', '-id']


class LikeDislikeMixin(models.Model):
    likes = models.ManyToManyField(
        User,
        related_name='%(class)s_likes',
        blank=True
    )
    dislikes = models.ManyToManyField(
        User,
        related_name='%(class)s_dislikes',
        blank=True
    )

    class Meta:
        abstract = True

    def like(self, user):
        self.un_dislike(user)
        self.likes.add(user)

    def un_like(self, user):
        self.likes.remove(user)

    def dislike(self, user):
        self.un_like(user)
        self.dislikes.add(user)

    def un_dislike(self, user):
        self.dislikes.remove(user)


class LikeDislikeTimeMixin(
    TimestampsBaseMixin,
    LikeDislikeMixin,
    models.Model
):
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True
    )

    class Meta:
        abstract = True


class BaseModelViewSet(viewsets.GenericViewSet):

    def get_serializer_class(self):
        return self.action_serializer_classes.get(self.action)


class MemModelViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      BaseModelViewSet):
    pass
