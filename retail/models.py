from django.db import models
from django.utils.translation import gettext_lazy as _


class Partner(models.Model):
    title = models.CharField(max_length=150, verbose_name=_("Title"))
    full_name = models.CharField(max_length=255, verbose_name=_("Full name"))

    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")

    def __str__(self):
        return self.title


class Shop(models.Model):
    title = models.CharField(unique=True, max_length=150, verbose_name=_("Title"))

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")

    def __str__(self):
        return self.title
