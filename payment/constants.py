from django.db import models


class PaymentState(models.TextChoices):
    """
    Enum for payment states.
    """

    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"
