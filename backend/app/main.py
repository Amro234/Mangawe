from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.models.database import init_db, seed_db
from backend.app.routers import products, orders, auth, users, logs
from backend.app.middleware.logs import BHM

@asynccontextmanager
async def startSpan(_app: FastAPI):
    print("Starting_API_MANGAWEE.....")
    init_db()
    seed_db()
    print("DB is done")
    yield
    print("Shutting_API_MANGAWEE.....")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=startSpan
)

#! Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BHM)

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(logs.router)

# *Root Health Check Route
@app.get("/", tags=["Health Check"])
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "status": "online",
        "docs_url": "/docs"
    }