from fastapi import APIRouter, Depends, HTTPException, Header, Query
from decimal import Decimal
from typing import Optional

from app.api.schemas import (
    DepositRequest,
    WithdrawRequest,
    TransferRequest,
    TransactionResponse,
    TransactionListResponse,
)
from app.core.database import get_db
from app.services.wallet_service import WalletService
from app.utils.exceptions import BusinessRuleError, NotFoundError
from app.repositories.transaction_repository import TransactionRepository

router = APIRouter()


def get_wallet_service(db=Depends(get_db)) -> WalletService:
    return WalletService(db)


@router.post("/wallet/deposit/", response_model=TransactionResponse)
def deposit(
    request: DepositRequest,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
    wallet_id: int = Query(...),
    service: WalletService = Depends(get_wallet_service),
):
    try:
        transaction = service.deposit(wallet_id, Decimal(request.amount), idempotency_key, request.description)
        return transaction
    except BusinessRuleError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/wallet/withdraw/", response_model=TransactionResponse)
def withdraw(
    request: WithdrawRequest,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
    wallet_id: int = Query(...),
    service: WalletService = Depends(get_wallet_service),
):
    try:
        transaction = service.withdraw(wallet_id, Decimal(request.amount), idempotency_key, request.description)
        return transaction
    except BusinessRuleError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/wallet/transfer/", response_model=TransactionResponse)
def transfer(
    request: TransferRequest,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
    service: WalletService = Depends(get_wallet_service),
):
    try:
        transaction = service.transfer(
            request.sender_wallet_id,
            request.recipient_wallet_id,
            Decimal(request.amount),
            idempotency_key,
            request.description,
        )
        return transaction
    except BusinessRuleError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/wallet/transactions/", response_model=TransactionListResponse)
def list_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    reference: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    min_amount: Optional[Decimal] = Query(None),
    max_amount: Optional[Decimal] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db=Depends(get_db),
):
    filters = {
        "reference": reference,
        "type": type,
        "status": status,
        "min_amount": min_amount,
        "max_amount": max_amount,
        "start_date": start_date,
        "end_date": end_date,
    }
    repo = TransactionRepository(db)
    transactions = repo.search(filters, offset=(page - 1) * page_size, limit=page_size)
    return TransactionListResponse(transactions=transactions)
