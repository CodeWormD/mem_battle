from rest_framework import serializers

from apps.mems.models import Mem


class MemsBattleListSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        model = Mem
        fields = (
            'id',
            'image',
            'owner',
            'created_at',
        )
