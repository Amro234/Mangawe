from fastapi import APIRouter, Depends , status , HTTPException, Response


router = APIRouter(
prefix = "/api/auth",
tags = ["Authentication"]
)

