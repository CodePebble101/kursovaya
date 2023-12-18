import logging
import smtplib

from celery import Celery

from email.message import EmailMessage
from app.config.config import RedisSettings

ADMIN_EMAIL = 'LEXINUS555@yandex.ru'
ADMIN_PASSWORD = 'upjadwsvetbcgswl'
SMTP_HOST = 'smtp.yandex.ru'
SMTP_PORT = 587

celery_worker = Celery("tasks", broker=f"redis://{RedisSettings.REDIS_HOST}:{RedisSettings.REDIS_PORT}")


@celery_worker.task()
def send_email(recipients: list, subject: str, content: str):
    print("Try to send message")
    msg = EmailMessage()
    msg['From'] = ADMIN_EMAIL
    msg['Bcc'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg.set_content(content)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as mailserver:
            mailserver.set_debuglevel(False)
            mailserver.starttls()
            mailserver.login(ADMIN_EMAIL, ADMIN_PASSWORD)
            mailserver.send_message(msg)
        logging.warning("Письмо успешно отправлено")

    except smtplib.SMTPException as ex:
        logging.error(f"Ошибка: Невозможно отправить сообщение. {ex}")
        raise Exception
