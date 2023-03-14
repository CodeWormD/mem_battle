from django.contrib import admin

from .models import Mem


@admin.register(Mem)
class MemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'image',
        'upload_data',
    )
    list_filter = ('id', 'upload_data')