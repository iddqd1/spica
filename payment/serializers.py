from typing import Any

from django.conf import settings
from rest_framework import serializers

from . import dtos
from . import gateways
from . import models


class StripePaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for StripePayment model.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    stripe_session_id = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = models.Payment
        fields = ["survey", "user", "id", "created", "modified", "stripe_session_id", "used", "state", "url", "amount"]
        read_only_fields = ("id", "created", "modified", "stripe_session_id", "used", "state", "url", "amount")

    def create(self, validated_data: Any) -> Any:
        stripe_checkout_response: dtos.StripeSessionResponse = gateways.create_stripe_checkout_session(
            settings.STRIPE_SECRET_KEY,
            models.StripePayment.build_stripe_checkout_data(validated_data["survey"]),
        )
        validated_data["amount"] = validated_data["survey"].price
        payment = super().create(validated_data)
        models.StripePayment.objects.create(
            payment=payment,
            stripe_session_id=stripe_checkout_response.id,
            url=stripe_checkout_response.url,
        )
        return payment

    def get_stripe_session_id(self, obj: models.Payment) -> str:
        """
        Get the Stripe session ID for the payment.
        """
        return obj.stripe_payment.stripe_session_id if hasattr(obj, "stripe_payment") else ""

    def get_url(self, obj: models.Payment) -> str:
        """
        Get the URL for the Stripe checkout session.
        """
        return obj.stripe_payment.url if hasattr(obj, "stripe_payment") else ""
