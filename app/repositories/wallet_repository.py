from sqlalchemy.orm import Session

from app.models.wallet import Wallet, WalletStatus
from app.utils.exceptions import NotFoundError


class WalletRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, wallet_id: int) -> Wallet:
        wallet = self.db.query(Wallet).filter(Wallet.id == wallet_id).one_or_none()
        if wallet is None:
            raise NotFoundError(f"Wallet {wallet_id} not found")
        return wallet

    def get_by_user_and_currency(self, user_id: int, currency: str) -> Wallet | None:
        return (
            self.db.query(Wallet)
            .filter(Wallet.user_id == user_id, Wallet.currency == currency)
            .one_or_none()
        )

    def save(self, wallet: Wallet) -> Wallet:
        self.db.add(wallet)
        self.db.flush()
        return wallet

    def freeze(self, wallet: Wallet) -> Wallet:
        wallet.status = WalletStatus.FROZEN
        self.db.add(wallet)
        self.db.flush()
        return wallet

    def unfreeze(self, wallet: Wallet) -> Wallet:
        wallet.status = WalletStatus.ACTIVE
        self.db.add(wallet)
        self.db.flush()
        return wallet
