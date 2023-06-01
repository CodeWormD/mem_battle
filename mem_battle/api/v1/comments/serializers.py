from rest_framework import serializers

from apps.mems.models import Comment


class ChildCommentsSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id',
                  'owner',
                  'created_at', 'text', 'parent', 'likes_count', 'dislikes_count')

    def get_likes_count(self, obj):
        return obj.likes_count

    def get_dislikes_count(self, obj):
        return obj.dislikes_count



class CommentListSerializer(serializers.ModelSerializer):
    threads = ChildCommentsSerializer(many=True, read_only=True)
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    parent = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id',
                  'owner',
                  'created_at',
                  'text',
                  'parent',
                  'likes_count', 'dislikes_count', 'threads')

    def get_likes_count(self, obj):
        return obj.likes_count

    def get_dislikes_count(self, obj):
        return obj.dislikes_count

    def get_parent(self, obj):
        return obj.parent_id


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for POST root comment"""
    class Meta:
        model = Comment
        fields = ('text',)


class CommentChildSerializer(serializers.ModelSerializer):
    """Serializer for POST Child comment"""
    class Meta:
        model = Comment
        fields = ('id', 'text',)