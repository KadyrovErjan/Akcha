from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширенная модель пользователя с полем дохода."""
    income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Ежемесячный доход'
    )

    def __str__(self):
        return self.username