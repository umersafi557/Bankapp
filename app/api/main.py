from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.core.database import init_db
from app.api.routes import router

app = FastAPI(title="BankApp Wallet Service")
app.include_router(router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>BankApp Wallet Service</title>
        <style>
            body {
                margin: 0;
                font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                background: #f4f7fb;
                color: #202b45;
            }
            header {
                background: linear-gradient(135deg, #2a58ff 0%, #00c2ff 100%);
                color: white;
                padding: 2rem 1.5rem;
                text-align: center;
                box-shadow: 0 16px 35px rgba(0, 37, 97, 0.12);
            }
            header h1 {
                margin: 0;
                font-size: 2.25rem;
            }
            header p {
                margin: 0.75rem auto 0;
                max-width: 720px;
                opacity: 0.85;
            }
            .container {
                max-width: 1140px;
                margin: -3rem auto 2rem;
                padding: 0 1rem;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                gap: 1.25rem;
            }
            .card {
                background: white;
                border-radius: 24px;
                border: 1px solid rgba(15, 23, 42, 0.08);
                box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
                padding: 1.5rem;
            }
            .card h2 {
                margin-top: 0;
                font-size: 1.25rem;
            }
            label {
                display: block;
                margin: 0.75rem 0 0.35rem;
                font-weight: 600;
            }
            input, textarea {
                width: 100%;
                padding: 0.95rem 1rem;
                border-radius: 14px;
                border: 1px solid #d8e0f2;
                background: #fbfdff;
                font-size: 0.98rem;
                color: #172026;
                box-sizing: border-box;
            }
            textarea {
                min-height: 90px;
                resize: vertical;
            }
            button {
                margin-top: 1rem;
                width: 100%;
                border: none;
                border-radius: 14px;
                padding: 1rem 1.25rem;
                font-size: 1rem;
                background: #1e3de0;
                color: white;
                cursor: pointer;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            button:hover {
                transform: translateY(-1px);
                box-shadow: 0 14px 28px rgba(30, 61, 224, 0.18);
            }
            .response {
                margin-top: 1rem;
                padding: 1rem;
                border-radius: 18px;
                background: #eff4ff;
                border: 1px solid #d0dcff;
                font-size: 0.95rem;
                line-height: 1.6;
                white-space: pre-wrap;
            }
            .note {
                margin: 0.5rem 0 0;
                color: #64748b;
                font-size: 0.95rem;
            }
            footer {
                text-align: center;
                padding: 1rem 0;
                color: #61779a;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>BankApp Wallet Service</h1>
            <p>Use this live dashboard to deposit, withdraw, transfer funds, and inspect transaction history on the BankApp backend.</p>
        </header>
        <div class="container">
            <div class="grid">
                <div class="card">
                    <h2>Deposit</h2>
                    <label for="deposit-wallet">Wallet ID</label>
                    <input id="deposit-wallet" type="number" placeholder="Enter wallet ID" value="1" />
                    <label for="deposit-amount">Amount</label>
                    <input id="deposit-amount" type="number" placeholder="5000" value="5000" />
                    <label for="deposit-desc">Description</label>
                    <textarea id="deposit-desc" placeholder="e.g. Salary credit"></textarea>
                    <button onclick="sendDeposit()">Deposit Funds</button>
                    <div id="deposit-response" class="response">Response will appear here.</div>
                </div>
                <div class="card">
                    <h2>Withdraw</h2>
                    <label for="withdraw-wallet">Wallet ID</label>
                    <input id="withdraw-wallet" type="number" placeholder="Enter wallet ID" value="1" />
                    <label for="withdraw-amount">Amount</label>
                    <input id="withdraw-amount" type="number" placeholder="2000" value="2000" />
                    <label for="withdraw-desc">Description</label>
                    <textarea id="withdraw-desc" placeholder="e.g. ATM withdrawal"></textarea>
                    <button onclick="sendWithdraw()">Withdraw Funds</button>
                    <div id="withdraw-response" class="response">Response will appear here.</div>
                </div>
                <div class="card">
                    <h2>Transfer</h2>
                    <label for="transfer-sender">Sender Wallet ID</label>
                    <input id="transfer-sender" type="number" placeholder="1" value="1" />
                    <label for="transfer-recipient">Recipient Wallet ID</label>
                    <input id="transfer-recipient" type="number" placeholder="2" value="2" />
                    <label for="transfer-amount">Amount</label>
                    <input id="transfer-amount" type="number" placeholder="3000" value="3000" />
                    <label for="transfer-desc">Description</label>
                    <textarea id="transfer-desc" placeholder="e.g. Payment for invoice"></textarea>
                    <button onclick="sendTransfer()">Send Transfer</button>
                    <div id="transfer-response" class="response">Response will appear here.</div>
                </div>
                <div class="card">
                    <h2>Transaction History</h2>
                    <label for="history-page">Page</label>
                    <input id="history-page" type="number" placeholder="1" value="1" />
                    <label for="history-page-size">Page Size</label>
                    <input id="history-page-size" type="number" placeholder="20" value="20" />
                    <button onclick="loadTransactions()">Load Transactions</button>
                    <div id="history-response" class="response">Response will appear here.</div>
                </div>
            </div>
        </div>
        <footer>Powered by BankApp backend API. Use wallet IDs from your database or seed data.</footer>
        <script>
            const baseUrl = window.location.origin;

            function randomId() {
                return Math.random().toString(36).slice(2) + Date.now().toString(36);
            }

            async function sendDeposit() {
                const walletId = document.getElementById('deposit-wallet').value;
                const amount = document.getElementById('deposit-amount').value;
                const description = document.getElementById('deposit-desc').value;
                const responseBox = document.getElementById('deposit-response');
                responseBox.textContent = 'Sending deposit...';

                const response = await fetch(`${baseUrl}/api/wallet/deposit/?wallet_id=${walletId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Idempotency-Key': randomId(),
                    },
                    body: JSON.stringify({ amount, description }),
                });
                const data = await response.json();
                responseBox.textContent = JSON.stringify(data, null, 2);
            }

            async function sendWithdraw() {
                const walletId = document.getElementById('withdraw-wallet').value;
                const amount = document.getElementById('withdraw-amount').value;
                const description = document.getElementById('withdraw-desc').value;
                const responseBox = document.getElementById('withdraw-response');
                responseBox.textContent = 'Sending withdrawal...';

                const response = await fetch(`${baseUrl}/api/wallet/withdraw/?wallet_id=${walletId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Idempotency-Key': randomId(),
                    },
                    body: JSON.stringify({ amount, description }),
                });
                const data = await response.json();
                responseBox.textContent = JSON.stringify(data, null, 2);
            }

            async function sendTransfer() {
                const sender = document.getElementById('transfer-sender').value;
                const recipient = document.getElementById('transfer-recipient').value;
                const amount = document.getElementById('transfer-amount').value;
                const description = document.getElementById('transfer-desc').value;
                const responseBox = document.getElementById('transfer-response');
                responseBox.textContent = 'Sending transfer...';

                const response = await fetch(`${baseUrl}/api/wallet/transfer/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Idempotency-Key': randomId(),
                    },
                    body: JSON.stringify({ sender_wallet_id: Number(sender), recipient_wallet_id: Number(recipient), amount, description }),
                });
                const data = await response.json();
                responseBox.textContent = JSON.stringify(data, null, 2);
            }

            async function loadTransactions() {
                const page = document.getElementById('history-page').value;
                const size = document.getElementById('history-page-size').value;
                const responseBox = document.getElementById('history-response');
                responseBox.textContent = 'Loading transactions...';

                const response = await fetch(`${baseUrl}/api/wallet/transactions/?page=${page}&page_size=${size}`);
                const data = await response.json();
                responseBox.textContent = JSON.stringify(data, null, 2);
            }
        </script>
    </body>
    </html>
    """


@app.get("/api")
@app.get("/api/")
def api_index() -> dict:
    return {
        "message": "Wallet API available",
        "endpoints": [
            "/api/wallet/deposit/",
            "/api/wallet/withdraw/",
            "/api/wallet/transfer/",
            "/api/wallet/transactions/",
        ],
    }


@app.on_event("startup")
def on_startup() -> None:
    init_db()
