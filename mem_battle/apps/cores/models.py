from django.db import models



class TimestampsBaseMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at','-id']



class TimestampsMixin(TimestampsBaseMixin):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at', '-id']
