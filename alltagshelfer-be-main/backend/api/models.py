# api/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _


class BlacklistedToken(models.Model):
    token = models.CharField(
        max_length=500, verbose_name=_('Blacklisted Token'))
    expiration_datetime = models.DateTimeField(verbose_name=_('Expiration'))

    def __str__(self):
        return self.token

    class Meta:
        verbose_name_plural = _('Blacklisted Tokens')
        verbose_name = _('Blacklisted Token')
