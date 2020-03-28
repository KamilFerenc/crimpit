from django.utils.translation import ugettext_lazy as _
from django.db import models


class TimeStampModel(models.Model):
    modified = models.DateTimeField(verbose_name=_('Created'), auto_now=True)
    created = models.DateTimeField(verbose_name=_('Created'), auto_now_add=True)

    class Meta:
        abstract = True
