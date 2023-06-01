from rest_framework import serializers

from apps.mems.models import Tag

from ..mems.serializers import MemsListSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class TagRetSerializer(serializers.ModelSerializer):
    mems = MemsListSerializer(many=True, read_only=True)
    class Meta:
        model = Tag
        fields = ('mems',)