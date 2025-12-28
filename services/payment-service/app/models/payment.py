from sqlalchemy import Column, Integer, String, Numeric, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, index=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, default="PENDING", index=True) # PENDING, SUCCESS, FAILED
    payment_method = Column(String, nullable=True)
    transaction_id = Column(String, nullable=True) # Gateway transaction ID
    idempotency_key = Column(String, unique=True, index=True, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
