# BankApp Wallet Service

A backend wallet system with a clear API, service layer, and repository layer.

## Features
- Wallet deposit, withdrawal, and transfer
- Idempotent transaction handling
- Business rules enforced in the service layer
- Transaction history with filtering and pagination

## Run
1. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic
   ```
2. Start the app:
   ```bash
   uvicorn app.api.main:app --reload
   ```

## Important Architecture
- `app/api` - request handling and response models
- `app/services` - business rules and transaction operations
- `app/repositories` - database access methods
- `app/models` - SQLAlchemy entities
