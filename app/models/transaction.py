import enum
from sqlalchemy import Column, Integer, String, Enum, Numeric, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models.base import Base


class TransactionType(str, enum.Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"
    ADJUSTMENT = "ADJUSTMENT"


class TransactionStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        UniqueConstraint("reference", name="uq_transaction_reference"),
    )

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, nullable=False, unique=True)
    idempotency_key = Column(String, nullable=True, index=True)
    type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(TransactionStatus), nullable=False, default=TransactionStatus.PENDING)
    amount = Column(Numeric(18, 2), nullable=False)
    currency = Column(String(length=3), nullable=False)
    source_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=True)
    destination_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    source_wallet = relationship("Wallet", foreign_keys=[source_wallet_id], back_populates="outgoing_transactions")
    destination_wallet = relationship("Wallet", foreign_keys=[destination_wallet_id], back_populates="incoming_transactions")
