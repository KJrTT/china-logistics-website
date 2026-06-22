from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime

def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    db_feedback = models.Feedback(
        name=feedback.name,
        contact=feedback.contact,
        message=feedback.message
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_feedbacks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Feedback).order_by(
        models.Feedback.created_at.desc()
    ).offset(skip).limit(limit).all()

def get_feedback(db: Session, feedback_id: int):
    return db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()

def update_feedback_status(db: Session, feedback_id: int, status: str):
    db_feedback = get_feedback(db, feedback_id)
    if db_feedback:
        db_feedback.status = status
        db_feedback.updated_at = datetime.now()
        if status == "completed":
            db_feedback.is_processed = True
        db.commit()
        db.refresh(db_feedback)
    return db_feedback