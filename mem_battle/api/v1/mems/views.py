from django.db.models import Count, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.cores.exceptions import MemDoesNotExist, MemListError
from apps.cores.filters import MemFilter
from apps.cores.mixins import LikeDislikeAPIView, MemModelViewSet
from apps.cores.permissions import IsOwnerOrReadOnly
from apps.mems.models import Mem, Tag
from apps.users.models import User

from .serializers import (MemCreateUpdateSerializer, MemDeleteSerializer,
                          MemRetriveSerializer, MemsListSerializer)


class MemsViewSet(MemModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = MemFilter
    search_fields = ['^tags__name', 'owner__username']
    ordering_fields = ['created_at', 'likes_count', 'vote_score']

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
            .only('owner__username', 'image', 'id', 'created_at', 'vote_score')
            .prefetch_related(
                Prefetch(
                    'tags',
                    queryset=Tag.objects.all()
                    .only('id', 'name')),
            )
            .annotate(likes_count=Count('likes', distinct=True),
                    dislikes_count=Count('dislikes', distinct=True),
                    com_count=Count('comments', distinct=True)
                    )
        )
        return queryset

    def get_object(self):
        instance = (
            Mem.objects
            .select_related('owner')
            .only('owner__username', 'image', 'id', 'created_at')
            .prefetch_related(
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
            ).get(id=self.kwargs['pk'])
        )
        return instance

    def list(self, request):
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except Exception:
            raise MemListError
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer_class()(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False,
            methods=["get"],
            url_path="user-mems",
            url_name="user-mems",
            permission_classes=[IsAuthenticated]
    )
    def own_user_list(self, request):
        queryset = self.filter_queryset(self.get_queryset().filter(owner=request.user))
        serializer = MemsListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        try:
            mem = self.get_object()
        except Mem.DoesNotExist:
            raise MemDoesNotExist
        self.check_object_permissions(self.request, mem)
        serializer = self.get_serializer_class()(mem, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            mem = self.get_object()
        except Mem.DoesNotExist:
            raise MemDoesNotExist
        self.check_object_permissions(self.request, mem)
        mem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MemLikeAPIView(LikeDislikeAPIView):
    """Add like for Mem instance"""
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            mem = self.get_object(obj=Mem)
        except Mem.DoesNotExist:
            raise MemDoesNotExist
        mem.like(user=request.user)
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            mem = self.get_object(obj=Mem)
        except Mem.DoesNotExist:
            raise MemDoesNotExist
        mem.un_like(user=request.user)
        return Response(status=status.HTTP_200_OK)


class MemDisLikeAPIView(LikeDislikeAPIView):
    """Add Dislike for Mem instance"""
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            mem = self.get_object(obj=Mem)
        except Mem.DoesNotExist:
            raise MemDoesNotExist
        mem.dislike(user=request.user)
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            mem = self.get_object(obj=Mem)
        except Mem.DoesNotExist:
            raise MemDoesNotExist
        mem.un_dislike(user=request.user)
        return Response(status=status.HTTP_200_OK)