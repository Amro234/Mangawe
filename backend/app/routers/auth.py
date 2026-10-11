from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from backend.app.core import security
from backend.app.models import usrs as user_model
from backend.app.schemas.usrs import (
    UsersRegister_Base,
    UserLogin_Base,
    UserResponse_Base,
)
from backend.app.schemas.token import TokenResponse_Base

router = APIRouter(
prefix = "/api/auth",
tags = ["Authentication"]
)

def parse_utc_timestamp(ts_str: Optional[str]) -> Optional[datetime]:
    if not ts_str:
        return None
    try:
        clean_str = ts_str.replace(" ", "T")
        dt = datetime.fromisoformat(clean_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None

def format_utc_timestamp(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

@router.post(
    "/register", 
    response_model=UserResponse_Base, 
    status_code=status.HTTP_201_CREATED
)
def register_user(user_data: UsersRegister_Base):
    existing_email = user_model.get_user_by_email(user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address is already registered"
        )

    existing_username = user_model.get_user_by_username(user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken"
        )
        
    hashed_pwd = security.hash_password(user_data.password)
    new_user = user_model.create_user(user_data, hashed_pwd)
    return new_user

@router.post("/login", response_model=TokenResponse_Base)
def login_user(credentials: UserLogin_Base):
    generic_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user = user_model.get_user_by_email(credentials.email)
    if not user:
        raise generic_error  
    
    if user["is_active"] == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account has been deactivated"
        )
        
    now = datetime.now(timezone.utc)
    
    locked_until_dt = parse_utc_timestamp(user.get("locked_until"))
    if locked_until_dt and now < locked_until_dt:
        remaining_seconds = int((locked_until_dt - now).total_seconds())
        remaining_minutes = max(1, remaining_seconds // 60)
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=f"Account temporarily locked due to multiple failed login attempts. Try again in {remaining_minutes} minute(s)."
        )

    is_valid_password = security.verify_password(credentials.password, user["hashed_password"])

    if not is_valid_password:
        # --- FAILED LOGIN ATTEMPT LOGIC ---
        attempts = user.get("failed_login_attempts") or 0
        window_start_dt = parse_utc_timestamp(user.get("failure_window_started_at"))
        lockout_level = user.get("lockout_level") or 0

        if not window_start_dt or (now - window_start_dt) > timedelta(minutes=15):
            attempts = 0
            window_start_dt = now

        attempts += 1

        if attempts >= 5:
            # Trigger Lockout
            lockout_level += 1
            # Exponential backoff: 1, 2, 4, 8, 16, max 30 minutes
            lock_minutes = min(30, 2 ** (lockout_level - 1))
            new_locked_until = now + timedelta(minutes=lock_minutes)

            user_model.update_lockout_state(
                user_id=user["id"],
                attempts=0,
                window_start=None,
                locked_until=format_utc_timestamp(new_locked_until),
                lockout_level=lockout_level
            )
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail=f"Too many failed login attempts. Account locked for {lock_minutes} minute(s)."
            )
        else:
            # Record failed attempt
            user_model.update_lockout_state(
                user_id=user["id"],
                attempts=attempts,
                window_start=format_utc_timestamp(window_start_dt),
                locked_until=None,
                lockout_level=lockout_level
            )
            raise generic_error
        
    user_model.reset_lockout_state(user["id"])

    # 6. Issue JWT Token
    token_payload = {
        "sub": user["email"],
        "user_id": user["id"],
        "role": user["role"]
    }
    token_str = security.create_access_token(token_payload)

    return TokenResponse_Base(access_token=token_str, token_type="bearer")