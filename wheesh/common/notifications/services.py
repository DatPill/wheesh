from django.conf import settings
from django.urls import reverse

from .interfaces import ServiceInterface
from .limiters import EmailLimiter
from .senders import EmailSender


class EmailVerificationService(ServiceInterface):
    def __init__(self, sender: EmailSender, limiter: EmailLimiter):
        self.sender: EmailSender = sender
        self.limiter: EmailLimiter = limiter

    def send_verification_web(self, user_id: int, user_email: str, username: str, code: int):
        if self.limiter.can_send(user_id):
            link: str = reverse('users:verify', args=(user_email, code))
            verification_link: str = f'{settings.DOMAIN_NAME}{link}'
            subject: str = f'Wheesh | Подтверждение регистрации для {username}'
            message: str = 'Привет, {}! Пожалуйста, перейдите по ссылке, чтобы подтвердить регистрацию.\n\n{}'.format(
                    username,
                    verification_link
            )

            self.sender.send(
                destination=user_email,
                subject=subject,
                message=message,
            )
        else:
            pass

    def send_verification_telegram(self, user_id, user_email, username, code):
        pass  # TODO
