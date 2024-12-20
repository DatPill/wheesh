from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def send_email(self):
        link = reverse('users:verify', args=(self.user.email, self.code))
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Wheesh | Подтверждение регистрации для {self.user.email}'
        message = 'Привет, {}! Пожалуйста, перейдите по ссылке, чтобы подтвердить регистрацию.\n\n{}'.format(
            self.user.username,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email='noreply@example.com',
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self) -> bool:
        return now() >= self.expiration

    def __str__(self) -> str:
        return f'EmailVerificationObject for {self.user.email}'

    class Meta:
        verbose_name = 'верификация эл. почты'
        verbose_name_plural = 'верификации эл. почты'
