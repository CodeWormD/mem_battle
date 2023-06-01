from django.db.models import Count, Prefetch
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from apps.cores.exceptions import (CommentDoesNotExist,
                                   CommentListDoesNotExists, MemDoesNotExist)
from apps.cores.mixins import (CommentCreateUpdateDestroyAPIView,
                               CommentListCreateAPIView, LikeDislikeAPIView)
from apps.cores.permissions import IsOwnerOrReadOnly
from apps.mems.models import Comment, Mem

from .serializers import (CommentChildSerializer, CommentListSerializer,
                          CommentSerializer)


class CommentListCreateAPIView(CommentListCreateAPIView):
    """Get list of mem's comments.
    Create root comment for mem instance"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    allowed_methods = {
        'POST': CommentSerializer,
        'GET': CommentListSerializer
    }

    def get_queryset(self, *args, **kwargs):
        mem = self.kwargs.get('mem_id')
        queryset = Comment.objects.select_related('owner').filter(mem=mem, parent=None).only(
            'id', 'mem', 'owner__username', 'created_at', 'text', 'parent__id'
        ).prefetch_related(Prefetch(
            'threads',
            Comment.objects.select_related('owner')
            .annotate(likes_count=Count('likes', distinct=True),
                    dislikes_count=Count('dislikes', distinct=True))
            )
        ).annotate(likes_count=Count('likes', distinct=True),
                    dislikes_count=Count('dislikes', distinct=True))
        return queryset

    def get_serializer_class(self):
        return self.allowed_methods[self.request.method]

    def list(self, request, *args, **kwargs):
        try:
            comments = self.get_queryset()
        except Exception:
            raise CommentListDoesNotExists
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = self.get_serializer_class()(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer_class()(comments, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            mem = Mem.objects.get(id=kwargs.get('mem_id'))
        except Mem.DoesNotExist:
            raise MemDoesNotExist
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user, mem=mem)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentCUDAPIView(CommentCreateUpdateDestroyAPIView):
    """Create child comment for root mems'comment.
    Updated and Destroy comment instance"""

    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        comment_id = self.kwargs.get('comment_id')
        instance = Comment.objects.get(id=comment_id)
        return instance

    def destroy(self, request, *args, **kwargs):
        try:
            comment = self.get_object()
        except Comment.DoesNotExist:
            raise CommentDoesNotExist
        self.check_object_permissions(self.request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        try:
            comment = self.get_object()
        except Comment.DoesNotExist:
            raise CommentDoesNotExist
        mem = Mem.objects.get(id=kwargs.get('mem_id'))
        if not comment.parent:
            serializer = CommentChildSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(parent=comment, mem=mem, owner=request.user)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            comment = self.get_object()
        except Comment.DoesNotExist:
            raise CommentDoesNotExist
        self.check_object_permissions(self.request, comment)
        serializer = self.serializer_class(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CommentLikeAPIView(LikeDislikeAPIView):
    """Add like for comment instance"""
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            comment = self.get_object(obj=Comment)
        except CommentDoesNotExist:
            raise CommentDoesNotExist
        comment.like(user=request.user)
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            comment = self.get_object(obj=Comment)
        except CommentDoesNotExist:
            raise CommentDoesNotExist
        comment.un_like(user=request.user)
        return Response(status=status.HTTP_200_OK)


class CommentDisLikeAPIView(LikeDislikeAPIView):
    """Add Dislike for comment instance"""
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            comment = self.get_object(obj=Comment)
        except CommentDoesNotExist:
            raise CommentDoesNotExist
        comment.dislike(user=request.user)
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            comment = self.get_object(obj=Comment)
        except CommentDoesNotExist:
            raise CommentDoesNotExist
        comment.un_dislike(user=request.user)
        return Response(status=status.HTTP_200_OK)