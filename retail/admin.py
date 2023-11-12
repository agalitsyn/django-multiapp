from django.contrib import admin

from .models import Partner, Report, ReportItem, Shop


@admin.register(Shop)
class ShopModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

    search_fields = ("slug", "title")
    ordering = ("title",)
    list_display = ("id", "title", "slug")


@admin.register(Partner)
class PartnerModelAdmin(admin.ModelAdmin):
    search_fields = [
        "title",
    ]
    ordering = ("title",)
    list_display = ("id", "title")


class ReportItemInline(admin.StackedInline):
    model = ReportItem
    extra = 0


@admin.register(Report)
class ReportModelAdmin(admin.ModelAdmin):
    ordering = ("-updated_at",)
    list_display = ("id", "shop", "started_at", "stopped_at", "created_at", "updated_at")

    inlines = (ReportItemInline,)
    fields = ("shop", "user", "started_at", "stopped_at")
