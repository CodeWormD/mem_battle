from django_filters import rest_framework as filters

from apps.mems.models import Mem


class CharFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class MemFilter(filters.FilterSet):
    tags = CharFilter(field_name="tags__name", lookup_expr='in')

    class Meta:
        model = Mem
        fields = ['tags']