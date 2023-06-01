from django.db.models import Count, Prefetch
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.cores.exceptions import TagDoesNotExist
from apps.cores.mixins import TagModelViewSet
from apps.mems.models import Mem, Tag

from .serializers import TagRetSerializer, TagSerializer


## !!! Подумать, как исключить retrieve
## и сделать на фронте при нажатии на тег
## обычную фильтрацию мемов
class TagViewSet(TagModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Tag.objects.annotate(count=Count('mems__id')).order_by('count').reverse()[:15]
    lookup_url_kwarg = 'slug'

    action_serializer_classes = {
        'retrieve': TagRetSerializer,
        'list': TagSerializer,
    }

    def get_object(self):
        instance = Tag.objects.prefetch_related(Prefetch('mems',
            queryset=Mem.objects
            .select_related('owner')
            .only('owner__username', 'image', 'id', 'created_at')
            .prefetch_related(
                Prefetch(
                    'tags',
                    queryset=Tag.objects.all()
                    .only('id', 'name')))
            .annotate(likes_count=Count('likes', distinct=True),
                    dislikes_count=Count('dislikes', distinct=True),
                    com_count=Count('comments', distinct=True))
            )).get(slug=self.kwargs['slug'])
        return instance

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Tag.DoesNotExist:
            raise TagDoesNotExist
        serializer = self.get_serializer_class()(instance)
        return Response(serializer.data)