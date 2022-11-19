from django.db import models


class DatesModelMixin(models.Model):
    """Abstract class for created/updated db model fields"""

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")
