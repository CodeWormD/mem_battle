from django.db.models import Count, Prefetch
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.v1.mems.serializers import MemsListSerializer
from apps.cores.exceptions import (FollowerDuplicationError,
                                   FollowyourselfError, MemListError,
                                   ProfileNotExistsError)
from apps.cores.mixins import ProfileUserMemsAPIView, UserFollowAPIView
from apps.mems.models import Mem, Tag
from apps.users.models import Follower, Profile, User

from .serializers import ProfileSerializer


class UserProfileFollowingMVS(UserFollowAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProfileSerializer

    def get_object(self):
        profile_id = self.kwargs['profile_id']
        try:
            profile = (Profile.objects
                    .annotate(subs=Count('owner__followed_by', distinct=True))
                    .get(id=profile_id))
            author = User.objects.get(profile=profile)
            return author
        except Profile.DoesNotExist:
            raise ProfileNotExistsError

    def follower_existing(self, request, author):
        return Follower.objects.filter(sender=request.user, receiver=author).exists()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        author = self.get_object()
        following = self.follower_existing(request, author)
        if following:
            raise FollowerDuplicationError
        if author == request.user:
            raise FollowyourselfError
        Follower.objects.create(sender=request.user, receiver=author)
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        author = self.get_object()
        following = self.follower_existing(request, author)
        if author != request.user and following:
            Follower.objects.filter(receiver=author, sender=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ProfileMemsAPIView(ProfileUserMemsAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.kwargs['profile_id']

    def get_queryset(self):
        author =  self.get_object()
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
                    com_count=Count('comments', distinct=True))
            .filter(owner__profile=author))
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            mems = self.filter_queryset(self.get_queryset())
        except Exception:
            raise MemListError
        page = self.paginate_queryset(mems)
        if page is not None:
            serializer = MemsListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MemsListSerializer(page, many=True)
        return Response(serializer.data)

# /v1/api/profile/id/ - get, (subscribe: post, delete)
# /v1/api/profile/id/mems/ - get (list)
