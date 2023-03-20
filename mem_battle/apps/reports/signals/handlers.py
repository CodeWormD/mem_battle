from django.db import models
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import os

from apps.mems.models import Mem


User = get_user_model()


@receiver(models.signals.post_delete, sender=Mem)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem
    when corresponding `Mem` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
            print(f"{instance.owner} удалил картинку")


@receiver(models.signals.post_save, sender=Mem)
def info_after_image_on_save(sender, instance, **kwargs):
    """
    Print info about user saved image.
    """
    if instance.image:
        print(f"{instance.owner} загрузил картинку")