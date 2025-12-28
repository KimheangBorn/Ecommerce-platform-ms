from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class PaymentCreate(BaseModel):
    order_id: str
    amount: Decimal
    payment_method: str = "credit_card"

class PaymentResponse(BaseModel):
    payment_id: str
    order_id: str
    amount: Decimal
    status: str
    transaction_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
