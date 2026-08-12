from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class DepositRequest(BaseModel):
    amount: Decimal = Field(..., gt=0)
    description: Optional[str] = None


class WithdrawRequest(BaseModel):
    amount: Decimal = Field(..., gt=0)
    description: Optional[str] = None


class TransferRequest(BaseModel):
    sender_wallet_id: int
    recipient_wallet_id: int
    amount: Decimal = Field(..., gt=0)
    description: Optional[str] = None


class TransactionResponse(BaseModel):
    reference: str
    type: str
    status: str
    amount: Decimal
    currency: str
    source_wallet_id: Optional[int]
    destination_wallet_id: Optional[int]
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionListResponse(BaseModel):
    transactions: list[TransactionResponse]
