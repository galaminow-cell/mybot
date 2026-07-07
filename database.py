import sqlite3
from datetime import datetime


class Database:

    def __init__(self, db_name="database.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Пользователи
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            tariff TEXT,
            expire_date TEXT,
            payment_status TEXT DEFAULT 'not_paid',
            created_at TEXT
        )
        """)

        # Заявки на оплату
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            tariff TEXT,
            amount INTEGER,
            payment_method TEXT,
            status TEXT DEFAULT 'waiting',
            created_at TEXT
        )
        """)

        self.conn.commit()

    # ---------------- USERS ----------------

    def add_user(self, telegram_id, username, first_name):
        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT OR IGNORE INTO users
        (
            telegram_id,
            username,
            first_name,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            telegram_id,
            username,
            first_name,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        self.conn.commit()

    def get_user(self, telegram_id):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT *
        FROM users
        WHERE telegram_id = ?
        """, (telegram_id,))

        return cursor.fetchone()

    def set_tariff(self, telegram_id, tariff, expire_date):
        cursor = self.conn.cursor()

        cursor.execute("""
        UPDATE users
        SET
            tariff = ?,
            expire_date = ?
        WHERE telegram_id = ?
        """,
        (
            tariff,
            expire_date,
            telegram_id
        ))

        self.conn.commit()

    def set_payment_status(self, telegram_id, status):
        cursor = self.conn.cursor()

        cursor.execute("""
        UPDATE users
        SET payment_status = ?
        WHERE telegram_id = ?
        """,
        (
            status,
            telegram_id
        ))

        self.conn.commit()

    def get_payment_status(self, telegram_id):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT payment_status
        FROM users
        WHERE telegram_id = ?
        """, (telegram_id,))

        row = cursor.fetchone()

        if row:
            return row[0]

        return None

    # ---------------- PAYMENTS ----------------

    def create_payment(
        self,
        telegram_id,
        tariff,
        amount,
        payment_method
    ):
        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT INTO payments
        (
            telegram_id,
            tariff,
            amount,
            payment_method,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            telegram_id,
            tariff,
            amount,
            payment_method,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        self.conn.commit()

        return cursor.lastrowid

    def get_payment(self, payment_id):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT *
        FROM payments
        WHERE id = ?
        """, (payment_id,))

        return cursor.fetchone()

    def update_payment_status(self, payment_id, status):
        cursor = self.conn.cursor()

        cursor.execute("""
        UPDATE payments
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            payment_id
        ))

        self.conn.commit()

    def get_waiting_payment(self, telegram_id):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT *
        FROM payments
        WHERE telegram_id = ?
        AND status = 'waiting'
        ORDER BY id DESC
        LIMIT 1
        """, (telegram_id,))

        return cursor.fetchone()

    def close(self):
        self.conn.close()