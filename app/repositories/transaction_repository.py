from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.transaction import Transaction, TransactionStatus, TransactionType


class TransactionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_idempotency_key(self, idempotency_key: str) -> Transaction | None:
        if not idempotency_key:
            return None
        return (
            self.db.query(Transaction)
            .filter(Transaction.idempotency_key == idempotency_key)
            .one_or_none()
        )

    def create(self, transaction: Transaction) -> Transaction:
        self.db.add(transaction)
        self.db.flush()
        return transaction

    def get_next_reference(self) -> str:
        today = datetime.utcnow().date().isoformat().replace("-", "")
        count = (
            self.db.query(func.count(Transaction.id))
            .filter(func.strftime("%Y%m%d", Transaction.created_at) == today)
            .scalar()
            or 0
        )
        return f"TXN-{today}-{count + 1:06d}"

    def search(self, filters: dict, offset: int = 0, limit: int = 50):
        query = self.db.query(Transaction)

        if search := filters.get("reference"):
            query = query.filter(Transaction.reference.ilike(f"%{search}%"))
        if type_filter := filters.get("type"):
            query = query.filter(Transaction.type == type_filter)
        if status_filter := filters.get("status"):
            query = query.filter(Transaction.status == status_filter)
        if min_amount := filters.get("min_amount"):
            query = query.filter(Transaction.amount >= min_amount)
        if max_amount := filters.get("max_amount"):
            query = query.filter(Transaction.amount <= max_amount)
        if start_date := filters.get("start_date"):
            query = query.filter(Transaction.created_at >= start_date)
        if end_date := filters.get("end_date"):
            query = query.filter(Transaction.created_at <= end_date)

        return query.order_by(Transaction.created_at.desc()).offset(offset).limit(limit).all()

    def get_daily_total_for_wallet(self, wallet_id: int, transaction_type: TransactionType, date):
        query = self.db.query(func.coalesce(func.sum(Transaction.amount), 0))
        query = query.filter(
            Transaction.source_wallet_id == wallet_id,
            Transaction.type == transaction_type,
            Transaction.created_at >= date,
        )
        return query.scalar() or 0
