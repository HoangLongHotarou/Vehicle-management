import math
import os
import random
from datetime import datetime, timedelta

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from .config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_FROM,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="views/templates"
)

def create_otp_confirm():
    digits = '0123456789'
    OTP = ''
    for i in range(4):
        OTP += digits[math.floor(random.random()*10)]
    return OTP

async def send_otp(subject: str, email_to: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html'
    )
    fm = FastMail(conf)
    html = 'send_otp.html'
    await fm.send_message(message, template_name=html)