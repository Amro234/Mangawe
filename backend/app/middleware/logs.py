import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from backend.app.models.database import get_db

class BHM(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        user_id = None
        ip_address = request.client.host if request.client else "127.0.0.1"
        method = request.method
        path = request.url.path
        response = await call_next(request)
        status_code = response.status_code
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)


        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO logs (user_id, ip_address, path, method, status_code, latency_ms)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,(user_id, ip_address, path, method, status_code, latency_ms)
                )
                conn.commit()
        except Exception as e:
            print(f"Logging Failed: {e}")
        return response    