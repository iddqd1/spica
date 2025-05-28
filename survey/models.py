"""Survey models for storing survey data and responses."""

from django.contrib.auth import get_user_model
from django.db import models


class Survey(models.Model):
    """
    Survey model to store survey data.
    """

    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(help_text="Description of the survey.")
    configuration = models.TextField(
        blank=False,
        help_text="Configuration of the survey in suveyjs JSON format.",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the survey was created.",
    )
    modified = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the survey was last updated.",
    )
    strategy = models.CharField(max_length=50, blank=True, default="")
    active = models.BooleanField(
        default=True,
        help_text="Indicates whether the survey is active or not.",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=20.0,
        help_text="Price of the survey.",
    )

    def __str__(self):
        return str(self.title)


class SurveyResponse(models.Model):
    """
    SurveyResponse model to store survey responses.
    """

    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name="responses",
        help_text="Survey to which the response belongs.",
    )
    response = models.TextField(
        blank=False,
        help_text="Response to the survey in suveyjs JSON format.",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the response was created.",
    )
    modified = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the response was last updated.",
    )
    ip_address = models.CharField(
        default="",
        blank=True,
        help_text="IP address of the user who submitted the response.",
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    report_file = models.FileField(
        upload_to="reports/%Y/%m/%d/",
        blank=True,
        null=True,
        help_text="File containing the report of the survey response.",
    )

    class Meta:
        verbose_name = "Survey Response"
        verbose_name_plural = "Survey Responses"
        ordering = ["-id"]

    def __str__(self):
        return f"#{self.pk} {self.survey.title} - {self.created_by} - {self.created}"
