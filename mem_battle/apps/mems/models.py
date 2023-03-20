from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from utils.mem_path_save import user_directory_path

User = get_user_model()


class Mem(models.Model):
    """Мемы"""

    image = models.ImageField('Изображение', upload_to=user_directory_path)
    owner = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='mems',
        on_delete=models.CASCADE,)
    upload_data = models.DateTimeField('Дата добавления', auto_now_add=True)


    def __str__(self):
        return f'{self.owner} загрузил мем'

    class Meta:
        verbose_name = 'Мем'
        verbose_name_plural = 'Мемы'
