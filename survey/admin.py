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
                    "configuration",
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


@admin.register(models.SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    """Survey response admin."""

    list_display = (
        "id",
        "survey",
        "created_by",
        "created",
        "modified",
    )
    search_fields = ("survey__title", "created_by__username")
    list_filter = ("created_by",)
    ordering = ("-created",)
    list_per_page = 20
    date_hierarchy = "created"
    readonly_fields = ("created", "modified")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "survey",
                    "response",
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
