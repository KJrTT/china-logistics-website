import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
import logging

logger = logging.getLogger(__name__)

def send_email(to_email: str, subject: str, body: str):
    try:
        if not settings.SMTP_HOST:
            logger.warning("SMTP не настроен")
            return False
        
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_FROM
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Письмо отправлено на {to_email}")
        return True
    except Exception as e:
        logger.error(f"Не удалось отправить письмо: {e}")
        return False

def send_feedback_notification(feedback: dict):
    subject = f"Новая заявка от {feedback['name']}"
    body = f"""
Новая заявка на сайте логистики

Имя: {feedback['name']}
Контакт: {feedback['contact']}
Сообщение: {feedback['message']}

Дата: {feedback.get('created_at', '')}
    """
    return send_email(settings.TO_EMAIL, subject, body)

def send_confirmation_to_user(feedback: dict):
    subject = "Ваша заявка принята"
    body = f"""
Здравствуйте, {feedback['name']}!

Спасибо за обращение в нашу компанию.
Ваша заявка принята и будет обработана в ближайшее время.

Ваше сообщение: {feedback['message']}

Мы свяжемся с вами в течение 24 часов.

С уважением,
Команда Логистика B2B
    """
    if '@' in feedback['contact'] and '.' in feedback['contact']:
        return send_email(feedback['contact'], subject, body)
    else:
        logger.info(f"Контакт {feedback['contact']} не является email")
        return False