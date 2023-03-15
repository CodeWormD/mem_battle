from django.db import models



class Mem(models.Model):
    """Мемы"""

    image = models.ImageField('Изображение', upload_to='mem/')
    upload_data = models.DateTimeField('Дата добавления', auto_now_add=True)


    def __str__(self):
        return f'Картинка {self.id} - {self.upload_data}'

    class Meta:
        verbose_name = 'Мем'
        verbose_name_plural = 'Мемы'