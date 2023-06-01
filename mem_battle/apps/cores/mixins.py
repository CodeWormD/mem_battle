import uuid

from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response

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
    action_serializer_classes = None

    def get_serializer_class(self):
        return self.action_serializer_classes.get(self.action)


class MemModelViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      BaseModelViewSet):
    pass


class TagModelViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      BaseModelViewSet):
    pass


class CommentCreateUpdateDestroyAPIView(mixins.CreateModelMixin,
                                        mixins.UpdateModelMixin,
                                        mixins.DestroyModelMixin,
                                        generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentListCreateAPIView(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LikeDislikeAPIView(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_object(self, obj):
        if 'comment_id' not in self.kwargs:
            mem = get_object_or_404(obj, id=self.kwargs['mem_id'])
            self.check_object_permissions(self.request, mem)
            return mem
        comment = get_object_or_404(obj, id=self.kwargs['comment_id'])
        self.check_object_permissions(self.request, comment)
        return comment