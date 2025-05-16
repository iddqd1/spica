from rest_framework import permissions
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from survey import models
from survey import serializers


class SurveyViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """Survey viewset."""

    serializer_class = serializers.SurveySerializer
    queryset = models.Survey.objects.filter(active=True)


class SurveyResponseViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    """Survey response viewset."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.SurveyResponseSerializer

    def get_queryset(self):
        return models.SurveyResponse.objects.filter(created_by=self.request.user)
