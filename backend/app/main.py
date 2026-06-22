from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
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

# Добавление глобального обработчика ошибок, тк без этого все ошибки не перехватывались сразу
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = [error['msg'].replace("Value error, ", "") for error in exc.errors()]
    error_message = '; '.join(error_messages)
    
    logging.error(f"Validation error: {error_message}")
    return JSONResponse(
        status_code=422,
        content={"detail": error_message}
    )

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://china-logistics-frontend.onrender.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "*"  
    ],
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