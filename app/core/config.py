from pydantic_settings import BaseSettings


class WalletConfig(BaseSettings):
    database_url: str = "sqlite:///./bankapp.db"
    max_deposit_amount: int = 100_000
    max_withdrawal_amount: int = 50_000
    max_daily_withdrawal: int = 100_000
    max_transfer_amount: int = 100_000
    max_daily_transfer: int = 500_000
    currency_codes: tuple[str, ...] = ("USD", "PKR")
    transaction_reference_prefix: str = "TXN"
    idempotency_header: str = "Idempotency-Key"


settings = WalletConfig()
