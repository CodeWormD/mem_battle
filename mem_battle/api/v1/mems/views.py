from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.mems.models import Group, Mem, Comment, Tag
from apps.users.models import User
from .serializers import (
    MemsListSerializer,
    CommentMemSerializer,
    MemRetriveSerializer,
    MemCreateUpdateSerializer,
    MemDeleteSerializer)
from django.db.models import Prefetch, Count
from apps.cores.mixins import MemModelViewSet
from apps.cores.permissions import IsOwnerOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('owner')
    serializer_class = CommentMemSerializer



class MemsViewSet(MemModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    action_serializer_classes = {
        'retrieve': MemRetriveSerializer,
        'list': MemsListSerializer,
        'create': MemCreateUpdateSerializer,
        'update': MemCreateUpdateSerializer,
        'destroy': MemDeleteSerializer
    }

    def get_queryset(self):
        queryset = (
            Mem.objects
            .select_related('owner')
            .only('owner__username', 'image', 'id', 'created_at')
            .prefetch_related(
                Prefetch(
                    'groups',
                    queryset=Group.objects.all()
                    .only('id', 'name')),
            )
            .annotate(likes_count=Count('likes', distinct=True),
                    dislikes_count=Count('dislikes', distinct=True),
                    com_count=Count('comments', distinct=True)
                    ) # закешировать кол-во
        )
        return queryset

    def get_single_obj(self):
        queryset = (
            Mem.objects
            .select_related('owner')
            .only('owner__username', 'image', 'id', 'created_at')
            .prefetch_related(
                Prefetch(
                    'groups',
                    queryset=Group.objects.all()
                    .only('id', 'name')),
                Prefetch(
                    'likes',
                    queryset=User.objects.all()
                    .only('id', 'username')),
                Prefetch(
                    'dislikes',
                    queryset=User.objects.all()
                    .only('id', 'username')),
                Prefetch(
                    'tags',
                    queryset=Tag.objects.all()
                    .only('id', 'name')),
            )
        )
        return queryset

    def get_object(self):
        mem = get_object_or_404(self.get_single_obj(), id=self.kwargs['pk'])
        return mem

    def list(self, request):
        print(self.__dict__)
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        mem = self.get_object()
        serializer = self.get_serializer_class()(mem)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        mem = self.get_object()
        serializer = self.get_serializer_class()(mem, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Mem, id=self.kwargs['pk'])
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
