from django.db import models
from django.conf import settings
from utils.mem_path_save import user_directory_path


class Mem(models.Model):
    """Мемы"""

    image = models.ImageField(
        'Изображение',
        upload_to=user_directory_path
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        related_name='mems',
        on_delete=models.SET(1)
    )
    upload_data = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True
    )


    class Meta:
        verbose_name = 'Мем'
        verbose_name_plural = 'Мемы'

    def __str__(self):
        return f'{self.owner} загрузил мем'
