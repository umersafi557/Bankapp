# BankApp Wallet API

A learning project for a wallet service built with **FastAPI, SQLAlchemy, and Pydantic**. The code is organized into API, service, repository, and model layers to keep HTTP handling separate from business rules and database access.

## Features

- Wallet deposits, withdrawals, and transfers
- Idempotent transaction handling
- Business rules in a service layer
- Transaction history with filtering and pagination
- SQLAlchemy-based persistence

## Tech stack

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic and pydantic-settings

## Getting started

### Requirements

- Python 3.10+ recommended
- pip

### 1. Clone the repository

```bash
git clone https://github.com/umersafi557/Bankapp.git
cd Bankapp
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn app.api.main:app --reload
```

Open the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Architecture

```text
app/
├── api/           # HTTP endpoints and request/response handling
├── core/          # Application configuration and shared core logic
├── models/        # Data models
├── repositories/  # Database access
├── services/      # Wallet and transaction business rules
└── utils/         # Shared utilities
```

## Development checklist

Before using this project with real money or real customer data, add and verify:

- Automated tests for deposits, withdrawals, transfers, and failure cases
- Authentication and authorization
- Database migrations and documented database configuration
- Transaction consistency and concurrency tests
- Structured logging and safe error handling
- Environment-based secrets and production settings

This repository is a learning project and should not be treated as production-ready financial software without a security and correctness review.

## Repository hygiene

Do not commit real customer information, credentials, API keys, or live database files. If a database file contains personal or sensitive information, remove it from version control and rotate any exposed secrets as appropriate.


## Security and correctness status

**Learning project only — not production-ready and not suitable for real funds or customer data.** Before any real-world use:

- Review and test idempotency handling, especially retries and concurrent requests. An idempotency key should be uniquely constrained and scoped appropriately.
- Add database transaction/concurrency tests to prove balances cannot become negative and transfers remain atomic.
- Add authentication and per-user authorization before exposing wallet endpoints.
- Configure database URLs and secrets through environment variables; never commit credentials or real customer records.
- The repository currently contains a tracked `bankapp.db` file. Review it locally for sensitive or real customer data. The new `.gitignore` prevents newly untracked database files from being added, but it does not remove an already tracked database. If it contains sensitive data, remove it from version control and rotate any exposed credentials as appropriate.
- Add database migrations and production-grade backups before relying on persistent data.
