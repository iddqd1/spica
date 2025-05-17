from django.contrib import admin

from . import models


@admin.register(models.Survey)
class SurveyAdmin(admin.ModelAdmin):
    """Survey admin."""

    list_display = (
        "id",
        "title",
        "description",
        "created",
        "modified",
        "active",
    )
    search_fields = ("title",)
    list_filter = ("active",)
    ordering = ("-created",)
    list_per_page = 20
    date_hierarchy = "created"
    readonly_fields = ("created", "modified")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "description",
                    "active",
                ),
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "created",
                    "modified",
                ),
            },
        ),
    )
