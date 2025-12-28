from fastapi import APIRouter, Depends, HTTPException, Header, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.models.payment import Payment
from app.utils.redis_service import check_idempotency_key, store_idempotency_response
from app.services.kafka_producer import kafka_producer
import uuid

router = APIRouter()

@router.post("", response_model=PaymentResponse, status_code=201)
async def process_payment(
    payment_data: PaymentCreate, 
    idempotency_key: str = Header(None),
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    # 1. Check Idempotency
    if idempotency_key:
        cached = check_idempotency_key(idempotency_key)
        if cached:
            return cached

    # 2. Save Payment to DB
    new_payment = Payment(
        order_id=payment_data.order_id,
        amount=payment_data.amount,
        payment_method=payment_data.payment_method,
        idempotency_key=idempotency_key,
        status="PENDING",
        transaction_id=str(uuid.uuid4()) # Simulate gateway tx id
    )
    
    db.add(new_payment)
    await db.commit()
    await db.refresh(new_payment)
    
    # 3. Simulate Gateway Logic (Random success/fail?)
    # For now, assume success
    new_payment.status = "SUCCESS"
    await db.commit()
    
    response = PaymentResponse.model_validate(new_payment).model_dump()

    # 4. Store Idempotency
    if idempotency_key:
        store_idempotency_response(idempotency_key, response)

    # 5. Publish Event (Background Task)
    event_payload = {
        "payment_id": str(new_payment.payment_id),
        "order_id": new_payment.order_id,
        "amount": float(new_payment.amount),
        "status": new_payment.status
    }
    
    topic = "payment-success" if new_payment.status == "SUCCESS" else "payment-failed"
    
    # Simple background task wrapper for async kafka publish
    # In real app, might want robust queue, but FastAPI background tasks work for simple cases
    # We call publish directly here for simplicity, or wrapped function
    await kafka_producer.publish(topic, event_payload)

    return new_payment
