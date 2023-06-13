from django.conf import settings
from rest_framework import serializers

from apps.mems.models import Comment, Mem, Tag
from apps.cores.exceptions import (MoreThan10Mems,)


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        model = Comment
        fields = ('id', 'owner', 'text', 'parent')


class MemsListSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes_count

    def get_dislikes_count(self, obj):
        return obj.dislikes_count

    def get_comments_count(self, obj):
        return obj.com_count


    class Meta:
        model = Mem
        fields = (
            'id',
            'image',
            'owner',
            'created_at',
            'comments_count',
            'likes_count',
            'dislikes_count',
            'vote_score',
            'tags',
        )


class MemRetriveSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    likes = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="username"
    )
    dislikes = serializers.SlugRelatedField(
        many=True,
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
            'tags',
            'likes',
            'dislikes',
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class MemCreateUpdateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(required=False)
    image = serializers.ListField(child=serializers.ImageField(), write_only=True)
    bad_tags = settings.BAD_TAGS

    class Meta:
        model = Mem
        fields = (
            'owner',
            'image',
            'tags',
        )

    def make_tags_list(self, tags):
        return [tag.strip().lower() for tag in tags['name'].split(',')]

    def get_or_create_tag(self, tag):
        if tag not in self.bad_tags:
            if not Tag.objects.filter(name=tag).exists():
                Tag.objects.create(name=tag)
            t = Tag.objects.get(name=tag)
            return t

    def add_tags_list_to_self(self, validated_data):
        tags = validated_data['tags']
        setattr(self, 'list_tags', self.make_tags_list(tags))

    def add_tag_to_mem_instance(self, mem):
        [mem.tags.add(self.get_or_create_tag(tag)) for tag in self.list_tags]

    def create(self, validated_data):
        images = validated_data['image']
        if len(images) > 10:
            raise MoreThan10Mems
        if 'tags' in validated_data:
            self.add_tags_list_to_self(validated_data=validated_data)
        for image in images:
            mem = Mem.objects.create(
                owner=validated_data['owner'],
                image=image
            )
            if hasattr(self, 'list_tags'):
                self.add_tag_to_mem_instance(mem)
        return mem

    def update(self, instance, validated_data):
        if 'tags' in validated_data:
            self.add_tags_list_to_self(validated_data=validated_data)
        instance.tags.clear()
        instance.save()
        if hasattr(self, 'list_tags'):
            self.add_tag_to_mem_instance(instance)
        return instance


class MemDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mem
        fields = ('id',)

