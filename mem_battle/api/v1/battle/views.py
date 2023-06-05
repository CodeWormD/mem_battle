import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

from apps.cores.exceptions import (BattleForMemsEnd, QuersetBattleError,
                                   QuerysetError)
from apps.mems.models import Mem
from .serializers import MemsBattleListSerializer


class MemBattleViewSet(ReadOnlyModelViewSet):
    serializer_class = MemsBattleListSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


    def get_queryset(self):
        """Exclude mems user has already seen"""
        try:
            ls = self.request.session['mem_seen']
            queryset = Mem.objects.values_list('id', flat=True).exclude(pk__in=ls)
            return queryset
        except Mem.DoesNotExist:
            raise QuersetBattleError

    def get_object(self):
        mem_id = self.kwargs['pk']
        instance = Mem.objects.get(id=mem_id)
        return instance

    def get_random_mems(self, queryset):
        """Generate two random mems and add them to the temporary list
        until refresh queryset or retrieve one of two mems
        """
        if not queryset or len(queryset) < 2:
            raise QuerysetError
        try:
            rand = random.sample(list(queryset), k=2)
            for i in range(2):
                self.request.session['until_retrieve'].append(str(rand[i]))
                self.request.session.modified = True
            return rand
        except Mem.DoesNotExist:
            raise BattleForMemsEnd

    def list(self, request):
        """Refresh temporary list and filter mems which user
        has not seen yet
        """
        request.session['until_retrieve'] = []
        request.session.modified = True

        rand = self.get_random_mems(self.get_queryset())

        try:
            queryset = Mem.objects.select_related('owner').filter(pk__in=list(rand))
            serializer = self.get_serializer_class()(queryset, many=True)
            return Response(serializer.data)
        except Mem.DoesNotExist:
            raise BattleForMemsEnd

    def retrieve(self, request, *args, **kwargs):
        """Add score to one of the two mems, both of them move 
        to the list 'mem_seen'
        """
        mem = self.get_object()
        until_retreive = self.request.session['until_retrieve']
        mem_seen = self.request.session['mem_seen']

        if str(mem) not in until_retreive:
            raise BattleForMemsEnd
        for i in until_retreive:
            if i not in mem_seen:
                mem_seen.append(i)
                self.request.session.modified = True

        mem.vote_score += 1
        mem.save()
        return Response({'success': 'You made a choice'})