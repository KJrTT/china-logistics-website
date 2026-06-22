from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app import crud, schemas
from app.database import get_db
from app.email_service import send_feedback_notification, send_confirmation_to_user
from app.config import settings

router = APIRouter(prefix="/api/feedback", tags=["feedback"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=schemas.FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    feedback: schemas.FeedbackCreate,
    db: Session = Depends(get_db)
):
    try:
        db_feedback = crud.create_feedback(db, feedback)
        
        feedback_data = {
            "name": feedback.name,
            "contact": feedback.contact,
            "message": feedback.message,
            "created_at": db_feedback.created_at.strftime("%d.%m.%Y %H:%M")
        }
        
        if settings.SEND_NOTIFICATION_TO_MANAGER:
            try:
                send_feedback_notification(feedback_data)
                logger.info(f"Notification sent to manager for feedback #{db_feedback.id}")
            except Exception as e:
                logger.error(f"Failed to send notification: {e}")
        
        if settings.SEND_CONFIRMATION_TO_USER:
            try:
                if '@' in feedback.contact and '.' in feedback.contact:
                    send_confirmation_to_user(feedback_data)
                    logger.info(f"Confirmation sent to {feedback.contact}")
            except Exception as e:
                logger.error(f"Failed to send confirmation: {e}")
        
        return db_feedback
        
    except Exception as e:
        logger.error(f"Error creating feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при создании заявки. Попробуйте позже."
        )