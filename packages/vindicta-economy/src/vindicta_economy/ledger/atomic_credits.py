import asyncio
import json
import sqlite3
import time

from pydantic import BaseModel, Field

# --- Models ---


class ComputeCreditTransaction(BaseModel):
    id: str  # UUID or unique ID
    agent_id: str
    action_type: str
    amount: float = Field(..., gt=0, description="Cost in Compute Credits")
    timestamp: float = Field(default_factory=time.time)
    metadata: dict = Field(default_factory=dict)


class AccountBalance(BaseModel):
    agent_id: str
    balance: float = Field(default=0.0, ge=0.0)
    last_updated: float = Field(default_factory=time.time)


# --- Ledger Implementation ---


class AtomicLedger:
    def __init__(self, db_path: str = "compute_ledger.db"):
        self.db_path = db_path
        self._lock = asyncio.Lock()
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Accounts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    agent_id TEXT PRIMARY KEY,
                    balance REAL NOT NULL CHECK(balance >= 0),
                    last_updated REAL
                )
            """)
            # Transactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    agent_id TEXT NOT NULL,
                    action_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    timestamp REAL,
                    metadata TEXT,
                    FOREIGN KEY(agent_id) REFERENCES accounts(agent_id)
                )
            """)
            conn.commit()

    async def get_balance(self, agent_id: str) -> float:
        """Get the current balance for an agent."""
        # SQLite queries are blocking, so we run them in a thread if needed,
        # but for simple implementations, we can just use the lock.
        # However, asyncio.Lock only protects against concurrent async tasks,
        # not blocking IO. We should use run_in_executor for SQLite calls
        # if we want true non-blocking behavior.
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._get_balance_sync, agent_id)

    def _get_balance_sync(self, agent_id: str) -> float:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT balance FROM accounts WHERE agent_id = ?", (agent_id,)
            )
            row = cursor.fetchone()
            return row[0] if row else 0.0

    async def record_transaction(self, transaction: ComputeCreditTransaction) -> bool:
        """
        Record a transaction and update the balance.
        Returns True if successful, False if insufficient funds.
        """
        async with self._lock:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(
                None, self._record_transaction_sync, transaction
            )

    def _record_transaction_sync(self, transaction: ComputeCreditTransaction) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                # check balance
                cursor.execute(
                    "SELECT balance FROM accounts WHERE agent_id = ?",
                    (transaction.agent_id,),
                )
                row = cursor.fetchone()
                current_balance = row[0] if row else 0.0

                if current_balance < transaction.amount:
                    return False  # Insufficient funds

                # Update balance
                new_balance = current_balance - transaction.amount
                cursor.execute(
                    """
                    UPDATE accounts SET balance = ?, last_updated = ? 
                    WHERE agent_id = ?
                """,
                    (new_balance, time.time(), transaction.agent_id),
                )

                if cursor.rowcount == 0:
                    # Account might need creation if we allow overdraft or seed logic,
                    # but here we require existing funds or seed.
                    # Let's assume accounts must be funded first. This function handles strictly spending.
                    return False

                # Log transaction
                cursor.execute(
                    """
                    INSERT INTO transactions (id, agent_id, action_type, amount, timestamp, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        transaction.id,
                        transaction.agent_id,
                        transaction.action_type,
                        transaction.amount,
                        transaction.timestamp,
                        json.dumps(transaction.metadata),
                    ),
                )

                conn.commit()
                return True
            except sqlite3.IntegrityError:
                conn.rollback()
                return False
            except Exception as e:
                conn.rollback()
                raise e

    async def credit_account(self, agent_id: str, amount: float):
        """Inject credits into an account (e.g. initial grant or reward)."""
        async with self._lock:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None, self._credit_account_sync, agent_id, amount
            )

    def _credit_account_sync(self, agent_id: str, amount: float):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO accounts (agent_id, balance, last_updated)
                VALUES (?, ?, ?)
                ON CONFLICT(agent_id) DO UPDATE SET
                balance = balance + ?,
                last_updated = ?
            """,
                (agent_id, amount, time.time(), amount, time.time()),
            )
            conn.commit()
