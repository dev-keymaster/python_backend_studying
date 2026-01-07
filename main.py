from enum import Enum
from pydantic import BaseModel, Field, model_validator


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    CRYPTO = "crypto"


class OrderItemModel(BaseModel):
    sku: str = Field(pattern=r"^[A-Z]{3}-\d{4}$")
    quantity: int = Field(ge=1)
    price_per_unit: float = Field(gt=0)


class OrderModel(BaseModel):
    order_id: int | str
    items: list[OrderItemModel] = Field(min_length=1)
    status: OrderStatus = OrderStatus.PENDING
    payment_method: PaymentMethod
    total_price: float = Field(gt=0)
    discount_code: str | None = None

    @model_validator(mode="after")
    def validate_business_rules(self) -> "OrderModel":
        calculated_total = sum(
            item.quantity * item.price_per_unit for item in self.items
        )
        if abs(self.total_price - calculated_total) > 0.01:
            raise ValueError(
                f"Price mismatch: Expected {calculated_total}, got {self.total_price}"
            )

        if (
            self.payment_method == PaymentMethod.CRYPTO
            and self.discount_code is not None
        ):
            raise ValueError("Discount codes cannot be applied to Crypto payments")

        return self
