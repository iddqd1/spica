from rest_framework import serializers

from . import models


class SurveySerializer(serializers.ModelSerializer[models.Survey]):
    class Meta:
        model = models.Survey
        fields = [
            "id",
            "title",
            "description",
            "configuration",
            "created",
            "modified",
        ]
        read_only_fields = fields
