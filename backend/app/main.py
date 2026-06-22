from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import feedback
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Логистика B2B API",
    description="API для обработки заявок с сайта логистики",
    version="1.0.0"
)

# ненавистные CORS-настройки 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(feedback.router)

@app.get("/")
async def root():
    return {
        "message": "Логистика B2B API",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}