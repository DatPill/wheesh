from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)


    def __str__(self) -> str:
        return self.username


    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
