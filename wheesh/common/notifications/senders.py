from django.conf import settings
from django.core.mail import send_mail

from .interfaces import SenderInterface


class EmailSender(SenderInterface):
    def send(self, destination: str, subject: str, message: str) -> None:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_ADDRESS,
            recipient_list=[destination],
            fail_silently=False,
        )
