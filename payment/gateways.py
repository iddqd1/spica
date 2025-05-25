import logging

import stripe

from payment import dtos

logger = logging.getLogger(__name__)


def create_stripe_checkout_session(
    secret_key: str,
    checkout_data: dtos.StripeSessionRequest,
) -> dtos.StripeSessionResponse:
    """Create a Stripe checkout session.

    Args:
        secret_key (str): stripe secret key for authentication.
        checkout_data (dtos.StripeSessionRequest): stripe checkout session request data.

    Returns:
        dtos.StripeSessionResponse: response from the Stripe API containing the session URL and ID.
    """
    stripe.api_key = secret_key
    checkout_session = stripe.checkout.Session.create(
        success_url=checkout_data.success_url,
        cancel_url=checkout_data.cancel_url,
        payment_method_types=checkout_data.payment_method_types,
        mode=checkout_data.mode,
        line_items=checkout_data.line_items,
    )
    return dtos.StripeSessionResponse(url=checkout_session.url, id=checkout_session.id)
