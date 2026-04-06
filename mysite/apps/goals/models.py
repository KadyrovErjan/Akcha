from django.db import models
from django.conf import settings


class Goal(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='goals'
    )
    title = models.CharField(max_length=255, verbose_name='Название цели')
    target_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Целевая сумма'
    )
    current_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Текущий прогресс'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True, verbose_name='Дедлайн')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    @property
    def progress_percent(self):
        if self.target_amount == 0:
            return 0
        return round(float(self.current_amount) / float(self.target_amount) * 100, 1)

    def __str__(self):
        return self.title