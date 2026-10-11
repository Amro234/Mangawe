from typing import Optional
from backend.app.models.database import get_db
from backend.app.schemas.usrs import UsersRegister_Base

def get_user_by_email(email: str) -> Optional[dict]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),))
        row = cursor.fetchone()
        return dict(row) if row else None
    

def get_user_by_username(username: str) -> Optional[dict]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username.strip(),))
        row = cursor.fetchone()
        return dict(row) if row else None
    
def create_user(user_data: UsersRegister_Base, hashed_password: str) -> dict:
    clean_email = user_data.email.strip().lower()
    role = "admin" if clean_email.endswith("@mangawe.com") else "customer"

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (username, email, hashed_password, phone, city, role)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_data.username.strip(),
                clean_email,
                hashed_password,
                user_data.phone,
                user_data.city,
                role
            )
        )
        conn.commit()

    return get_user_by_email(clean_email)

def update_lockout_state(
    user_id: int, 
    attempts: int, 
    window_start: Optional[str], 
    locked_until: Optional[str], 
    lockout_level: int
):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users 
            SET failed_login_attempts = ?, 
                failure_window_started_at = ?, 
                locked_until = ?, 
                lockout_level = ?
            WHERE id = ?
            """,
            (attempts, window_start, locked_until, lockout_level, user_id)
        )
        conn.commit()

def reset_lockout_state(user_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users 
            SET failed_login_attempts = 0, 
                failure_window_started_at = NULL, 
                locked_until = NULL, 
                lockout_level = 0
            WHERE id = ?
            """,
            (user_id,)
        )
        conn.commit()