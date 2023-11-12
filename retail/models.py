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
    title = models.CharField(max_length=150, verbose_name=_("Title"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")

    def __str__(self):
        return self.title


class Report(models.Model):
    user = models.ForeignKey("core.User", on_delete=models.PROTECT, related_name="reports", verbose_name=_("Seller"))
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT, related_name="reports", verbose_name=_("Shop"))

    started_at = models.DateTimeField(verbose_name=_("Shift start"))
    stopped_at = models.DateTimeField(verbose_name=_("Shift stop"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated"))

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")

    def __str__(self):
        return str(self.pk)

    @property
    def total(self):
        total = 0
        for item in self.items.all():
            total += item.quantity
        return total


class ReportItemType(models.TextChoices):
    SALE = "sale", _("Sale")
    RETURN = "return", _("Return")


class ReportItemPaymentType(models.TextChoices):
    CARD = "card", _("Card")
    CASH = "cash", _("Cash")


class ReportItem(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="items", verbose_name=_("Report"))
    type = models.CharField(max_length=10, choices=ReportItemType, default=ReportItemType.SALE)
    payment = models.CharField(max_length=10, choices=ReportItemPaymentType, default=ReportItemPaymentType.CARD)
    barcode = models.DecimalField(max_digits=13, decimal_places=0, blank=False, null=False, verbose_name=_("Barcode"))
    quantity = models.PositiveIntegerField(default=1, blank=False, null=False, verbose_name=_("Quantity"))
    receipt = models.FileField(blank=True, upload_to="retail-report-receipts/%Y/%m/%d/")
