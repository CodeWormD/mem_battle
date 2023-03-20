from django.contrib import admin

from .models import Mem


@admin.register(Mem)
class MemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'image',
        'upload_data',
    )
    list_filter = ('owner', 'upload_data')