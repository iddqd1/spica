from django.contrib.auth import get_user_model
from django.db import models

from payment import constants
from survey import models as survey_models

from . import dtos


class Payment(models.Model):
    """
    Model to store Stripe payment information.
    """

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="stripe_payments",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    survey = models.ForeignKey(
        "survey.Survey",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    used = models.BooleanField(default=False)
    state = models.CharField(max_length=30, choices=constants.PaymentState.choices, default=constants.PaymentState.PENDING)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment #{self.id}  - {self.amount} {self.currency}"


class StripePayment(models.Model):
    """
    Model to store Stripe payment information.
    Inherits from Payment to add Stripe-specific fields.
    """

    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE,
        related_name="stripe_payment",
    )
    stripe_session_id = models.CharField(max_length=255, unique=True)
    url = models.CharField(max_length=4000)

    def __str__(self):
        return f"StripePayment #{self.id} {self.stripe_session_id}"

    @staticmethod
    def build_stripe_checkout_data(survey: survey_models.Survey) -> dtos.StripeSessionRequest:
        """
        Build the data required for Stripe checkout session.
        """
        return dtos.StripeSessionRequest(
            line_items=[
                dtos.LineItem(
                    price_data=dtos.PriceData(
                        currency="usd",
                        product_data={"name": survey.title},
                        unit_amount=int(survey.price * 100),  # Convert to cents
                    ),
                    quantity=1,
                ).model_dump(),
            ],
            mode="payment",
            success_url="http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8000/cancelled",
        )
