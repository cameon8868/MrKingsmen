import sqlite3

DATABASE_NAME = "bot_data.db"

def init_db():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS users") # Explicitly drop table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                address TEXT,
                phone_number TEXT,
                has_agreed_privacy INTEGER DEFAULT 0,
                qr_code BLOB DEFAULT NULL
            )
        """)
        conn.commit()

def get_user_info(user_id: int) -> tuple[str | None, str | None, bool]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT address, phone_number, has_agreed_privacy FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        if result:
            return result[0], result[1], bool(result[2])
        return None, None, False

def save_user_info(user_id: int, address: str | None, phone_number: str | None, has_agreed_privacy: bool | None = None):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        if has_agreed_privacy is not None:
            cursor.execute("INSERT OR REPLACE INTO users (id, address, phone_number, has_agreed_privacy) VALUES (?, ?, ?, ?)", (user_id, address, phone_number, int(has_agreed_privacy)))
        else:
            # If consent is not explicitly provided, fetch existing or default to 0
            existing_info = get_user_info(user_id)
            existing_consent = existing_info[2] if existing_info else False
            cursor.execute("INSERT OR REPLACE INTO users (id, address, phone_number, has_agreed_privacy) VALUES (?, ?, ?, ?)", (user_id, address, phone_number, int(existing_consent)))
        conn.commit()

def update_user_consent(user_id: int, consent: bool):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET has_agreed_privacy = ? WHERE id = ?", (int(consent), user_id))
        conn.commit()

def get_all_user_ids() -> list[int]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users")
        return [row[0] for row in cursor.fetchall()]

def save_qr_code(user_id: int, qr_code_data: bytes):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET qr_code = ? WHERE id = ?", (qr_code_data, user_id))
        conn.commit()

def get_qr_code(user_id: int) -> bytes | None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT qr_code FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None
