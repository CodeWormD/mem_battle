# Generated by Django 4.1.7 on 2023-03-19 08:27

from django.db import migrations, models
import apps.mems.models


class Migration(migrations.Migration):

    dependencies = [
        ('mems', '0002_alter_mem_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mem',
            name='image',
            field=models.ImageField(upload_to=apps.mems.models.user_directory_path, verbose_name='Изображение'),
        ),
    ]