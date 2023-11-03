from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RetailConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "retail"
    verbose_name = _("Retail")
