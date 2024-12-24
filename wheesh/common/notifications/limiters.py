from datetime import timedelta

from django.conf import settings
from django.utils.timezone import now
from users.models import EmailVerification

from .interfaces import LimiterInterface


class EmailLimiter(LimiterInterface):
    def __init__(self):
        self.limit = settings.EMAIL_LIMIT
        self.period = settings.LIMIT_PERIOD


    def can_send(self, user_id) -> bool:
        one_hour_ago = now() - timedelta(hours=1)
        verifications_count: int = EmailVerification.objects.filter(user_id=user_id, created__gte=one_hour_ago).count()

        if verifications_count <= self.limit:
            return True

        return False
