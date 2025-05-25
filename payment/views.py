from django.db.models.query import QuerySet
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from . import models
from . import serializers


class StripePaymentView(CreateModelMixin, GenericViewSet):
    """
    View to handle Stripe payment creation.
    """

    serializer_class = serializers.StripePaymentSerializer

    def get_queryset(self) -> QuerySet:
        return models.Payment.objects.filter(user=self.request.user)
