from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.cores.permissions import IsOwnerOrReadOnly
from apps.mems.models import Group
from apps.users.models import User


class GroupModelViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    action_serializer_classes = {
        'retrieve': ...,
        'list': ...,
        'create': ...,
        'update': ...,
        'destroy': ...
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_object(self):
        return super().get_object()

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)