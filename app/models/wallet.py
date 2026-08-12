import enum
from sqlalchemy import Column, Integer, ForeignKey, String, Enum, Numeric, DateTime, func
from sqlalchemy.orm import relationship

from app.models.base import Base


class WalletStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(Numeric(18, 2), nullable=False, default=0)
    currency = Column(String(length=3), nullable=False)
    status = Column(Enum(WalletStatus), nullable=False, default=WalletStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="wallets")
    outgoing_transactions = relationship("Transaction", foreign_keys="Transaction.source_wallet_id", back_populates="source_wallet")
    incoming_transactions = relationship("Transaction", foreign_keys="Transaction.destination_wallet_id", back_populates="destination_wallet")
