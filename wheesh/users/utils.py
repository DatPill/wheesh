from datetime import timedelta
from random import randint

from common.notifications import EmailLimiter, EmailSender, EmailVerificationService
from django.utils.timezone import now
from users.models import EmailVerification, User

email_sender = EmailSender()
rate_limiter = EmailLimiter()
email_verification_service = EmailVerificationService(email_sender, rate_limiter)


def generate_verification_code(length: int=4):
    code = randint(1000, int('9'*length))
    return code


def create_verification_object(user_id: int, code: int) -> EmailVerification:
    expiration = now() + timedelta(hours=48)
    verivication_obj = EmailVerification.objects.create(code=code, user_id=user_id, expiration=expiration)
    return verivication_obj
