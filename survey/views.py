from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from survey import models
from survey import serializers


class SurveyViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """Survey viewset."""

    serializer_class = serializers.SurveySerializer
    queryset = models.Survey.objects.filter(active=True)
