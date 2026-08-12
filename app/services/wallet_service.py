from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.wallet import Wallet, WalletStatus
from app.models.transaction import Transaction, TransactionStatus, TransactionType
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.wallet_repository import WalletRepository
from app.utils.exceptions import BusinessRuleError, NotFoundError


class WalletService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.wallet_repo = WalletRepository(db)
        self.transaction_repo = TransactionRepository(db)

    def get_wallet(self, wallet_id: int) -> Wallet:
        return self.wallet_repo.get_by_id(wallet_id)

    def deposit(self, wallet_id: int, amount: Decimal, idempotency_key: str | None = None, description: str | None = None) -> Transaction:
        if amount <= 0:
            raise BusinessRuleError("Amount must be greater than zero")
        if amount > settings.max_deposit_amount:
            raise BusinessRuleError("Deposit amount exceeds maximum limit")

        wallet = self.wallet_repo.get_by_id(wallet_id)
        self._validate_wallet_is_active(wallet)

        existing = self.transaction_repo.get_by_idempotency_key(idempotency_key or "")
        if existing:
            return existing

        transaction = Transaction(
            reference=self.transaction_repo.get_next_reference(),
            idempotency_key=idempotency_key,
            type=TransactionType.DEPOSIT,
            status=TransactionStatus.PENDING,
            amount=amount,
            currency=wallet.currency,
            destination_wallet_id=wallet.id,
            description=description,
        )

        try:
            wallet.balance += amount
            self.db.add(wallet)
            self.transaction_repo.create(transaction)
            transaction.status = TransactionStatus.COMPLETED
            self.db.commit()
            return transaction
        except Exception as exc:
            self.db.rollback()
            transaction.status = TransactionStatus.FAILED
            self.db.add(transaction)
            self.db.commit()
            raise BusinessRuleError("Deposit failed", details=str(exc))

    def withdraw(self, wallet_id: int, amount: Decimal, idempotency_key: str | None = None, description: str | None = None) -> Transaction:
        if amount <= 0:
            raise BusinessRuleError("Amount must be greater than zero")
        if amount > settings.max_withdrawal_amount:
            raise BusinessRuleError("Withdrawal amount exceeds maximum limit")

        wallet = self.wallet_repo.get_by_id(wallet_id)
        self._validate_wallet_is_active(wallet)

        if amount > wallet.balance:
            raise BusinessRuleError("Insufficient balance")

        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        withdrawn_today = self.transaction_repo.get_daily_total_for_wallet(wallet_id, TransactionType.WITHDRAWAL, today_start)
        if withdrawn_today + amount > settings.max_daily_withdrawal:
            raise BusinessRuleError("Daily withdrawal limit exceeded")

        existing = self.transaction_repo.get_by_idempotency_key(idempotency_key or "")
        if existing:
            return existing

        transaction = Transaction(
            reference=self.transaction_repo.get_next_reference(),
            idempotency_key=idempotency_key,
            type=TransactionType.WITHDRAWAL,
            status=TransactionStatus.PENDING,
            amount=amount,
            currency=wallet.currency,
            source_wallet_id=wallet.id,
            description=description,
        )

        try:
            wallet.balance -= amount
            self.db.add(wallet)
            self.transaction_repo.create(transaction)
            transaction.status = TransactionStatus.COMPLETED
            self.db.commit()
            return transaction
        except Exception as exc:
            self.db.rollback()
            transaction.status = TransactionStatus.FAILED
            self.db.add(transaction)
            self.db.commit()
            raise BusinessRuleError("Withdrawal failed", details=str(exc))

    def transfer(self, sender_wallet_id: int, receiver_wallet_id: int, amount: Decimal, idempotency_key: str | None = None, description: str | None = None) -> Transaction:
        if sender_wallet_id == receiver_wallet_id:
            raise BusinessRuleError("Sender and receiver wallets must be different")
        if amount <= 0:
            raise BusinessRuleError("Amount must be greater than zero")
        if amount > settings.max_transfer_amount:
            raise BusinessRuleError("Transfer amount exceeds maximum limit")

        sender_wallet = self.wallet_repo.get_by_id(sender_wallet_id)
        receiver_wallet = self.wallet_repo.get_by_id(receiver_wallet_id)
        self._validate_wallet_is_active(sender_wallet)
        self._validate_wallet_is_active(receiver_wallet)

        if sender_wallet.currency != receiver_wallet.currency:
            raise BusinessRuleError("Wallet currencies must match")
        if amount > sender_wallet.balance:
            raise BusinessRuleError("Insufficient balance")

        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        transferred_today = self.transaction_repo.get_daily_total_for_wallet(sender_wallet_id, TransactionType.TRANSFER, today_start)
        if transferred_today + amount > settings.max_daily_transfer:
            raise BusinessRuleError("Daily transfer limit exceeded")

        existing = self.transaction_repo.get_by_idempotency_key(idempotency_key or "")
        if existing:
            return existing

        transaction = Transaction(
            reference=self.transaction_repo.get_next_reference(),
            idempotency_key=idempotency_key,
            type=TransactionType.TRANSFER,
            status=TransactionStatus.PENDING,
            amount=amount,
            currency=sender_wallet.currency,
            source_wallet_id=sender_wallet.id,
            destination_wallet_id=receiver_wallet.id,
            description=description,
        )

        try:
            sender_wallet.balance -= amount
            receiver_wallet.balance += amount
            self.db.add(sender_wallet)
            self.db.add(receiver_wallet)
            self.transaction_repo.create(transaction)
            transaction.status = TransactionStatus.COMPLETED
            self.db.commit()
            return transaction
        except Exception as exc:
            self.db.rollback()
            transaction.status = TransactionStatus.FAILED
            self.db.add(transaction)
            self.db.commit()
            raise BusinessRuleError("Transfer failed", details=str(exc))

    def _validate_wallet_is_active(self, wallet: Wallet) -> None:
        if wallet.status != WalletStatus.ACTIVE:
            raise BusinessRuleError("Wallet is not active")
