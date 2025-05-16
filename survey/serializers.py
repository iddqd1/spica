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


class SurveyResponseSerializer(serializers.ModelSerializer[models.SurveyResponse]):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.SurveyResponse
        fields = [
            "id",
            "survey",
            "response",
            "created",
            "modified",
            "ip_address",
            "created_by",
        ]
        read_only_fields = [
            "id",
            "created",
            "modified",
            "ip_address",
            "created_by",
        ]

    def create(self, validated_data):
        validated_data["ip_address"] = self.context.get("request").META.get(
            "REMOTE_ADDR",
        )
        return super().create(validated_data)
