"""Payment tests"""

import random
from decimal import Decimal

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from payment import dtos
from payment import gateways


class TestStripeGateway:
    @pytest.mark.skip("Skipping tests for StripePaymentSerializer as it requires a real Stripe API key")
    def test_int_stripe_call(self):
        checkout_request = dtos.StripeSessionRequest(
            line_items=[
                dtos.LineItem(
                    price_data=dtos.PriceData(
                        currency="usd",
                        product_data={"name": "T-shirt"},
                        unit_amount=Decimal(2000),  # Amount in cents
                    ),
                    quantity=1,
                ).model_dump(),
            ],
            mode="payment",
            success_url="http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8000/cancelled",
        )

        gateways.create_stripe_checkout_session(settings.STRIPE_SECRET_KEY, checkout_request)


@pytest.mark.django_db
class TestIntegrationStripePaymentViews:
    @pytest.mark.skip("Skipping tests for StripePaymentSerializer as it requires a real Stripe API key")
    def test_int_stripe_payment_view(self, client_authenticated, surveys):
        survey = random.choice(surveys)  # noqa: S311
        response = client_authenticated.post(
            reverse("api:payment:stripe-checkout-list"),
            {
                "survey": survey.id,
            },
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert "stripe_session_id" in response.data
        assert "id" in response.data
        assert "url" in response.data
        assert "stripe_session_id" in response.data
        assert "created" in response.data
        assert "modified" in response.data

    def test_stripe_payment_view(self, client_authenticated, surveys, mocker):
        mocker.patch(
            "payment.gateways.create_stripe_checkout_session",
            return_value=dtos.StripeSessionResponse(
                url="http://example.com/checkout",
                id="cs_test_1234567890",
            ),
        )
        survey = random.choice(surveys)  # noqa: S311
        response = client_authenticated.post(
            reverse("api:payment:stripe-checkout-list"),
            {
                "survey": survey.id,
            },
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert "stripe_session_id" in response.data
        assert "id" in response.data
        assert "url" in response.data
        assert "stripe_session_id" in response.data
        assert "created" in response.data
        assert "modified" in response.data
