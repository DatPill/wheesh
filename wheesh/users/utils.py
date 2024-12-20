from datetime import timedelta
from uuid import uuid4

from django.utils.timezone import now
from users.models import EmailVerification, User


def send_verification_email(user: User) -> None:
    time_now  = now()
    one_hour_ago = time_now - timedelta(hours=1)
    verifications_count: int = EmailVerification.objects.filter(user=user, created__gte=one_hour_ago).count()

    if verifications_count <= 3:
        expiration = time_now + timedelta(hours=48)
        record = EmailVerification.objects.create(code=uuid4(), user=user, expiration=expiration)
        record.send_email()
