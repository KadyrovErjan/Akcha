from django.db import models
from django.conf import settings


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Еда'),
        ('transport', 'Транспорт'),
        ('fun', 'Развлечения'),
        ('education', 'Образование'),
        ('other', 'Другое'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    title = models.CharField(max_length=255, verbose_name='Название')
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма'
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name='Категория'
    )
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    note = models.TextField(blank=True, null=True, verbose_name='Заметка')

    class Meta:
        ordering = ['-date']
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'

    def __str__(self):
        return f'{self.title} — {self.amount}'