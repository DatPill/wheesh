from django.contrib.auth.models import AbstractUser
from django.db import models
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
    code = models.SmallIntegerField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def is_expired(self) -> bool:
        return now() >= self.expiration

    def __str__(self) -> str:
        return f'EmailVerificationObject for {self.user.email}'

    class Meta:
        verbose_name = 'верификация эл. почты'
        verbose_name_plural = 'верификации эл. почты'
        unique_together = ('code', 'user')
