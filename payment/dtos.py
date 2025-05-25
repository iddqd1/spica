from pydantic import BaseModel
from pydantic import Field


class PriceData(BaseModel):
    currency: str
    product_data: dict
    unit_amount: int


class LineItem(BaseModel):
    price_data: PriceData
    quantity: int


class StripeSessionRequest(BaseModel):
    line_items: list[dict]
    mode: str
    success_url: str
    cancel_url: str
    payment_method_types: list[str] = Field(default_factory=lambda: ["card"])


class StripeSessionResponse(BaseModel):
    url: str
    id: str
