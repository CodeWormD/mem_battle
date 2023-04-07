from django.contrib import admin

from apps.users.models import User

from .models import Comment, Group, Mem, Tag


@admin.register(Mem)
class MemAdmin(admin.ModelAdmin):
    model = Mem
    list_display = (
        'id',
        'owner',
        'image',
        'vote_score',
        'created_at',
        'mem_tags_count',
        'mem_comments_count',
        'mem_likes_count',
        'mem_dislikes_count'
    )
    list_filter = (
        'created_at',
        'owner', 'tags', 'vote_score')

    def mem_tags_count(self, obj):
        return obj.tags.count()

    def mem_comments_count(self, obj):
        return obj.comments.count()

    def mem_likes_count(self, obj):
        return obj.likes.count()

    def mem_dislikes_count(self, obj):
        return obj.dislikes.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name',
        'slug',
    )
    list_filter = (
        'name', 'slug',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'text',
        'parent',
        'mem',
    )
    list_filter = (
        'created_at', 'owner',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'name',
        'slug',
        'owner',
        'group_members_count',
        'group_mems_count',
    )
    filter_horizontal = ('members',)
    list_filter = ('owner',)


    def group_members_count(self, obj):
        return obj.members.count()

    def group_mems_count(self, obj):
        return obj.mems_group.count()
