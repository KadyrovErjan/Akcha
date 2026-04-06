from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Sum
from apps.finance.models import Expense
from apps.goals.models import Goal
from decimal import Decimal


class StatsView(APIView):
    """Аналитика: расходы, остаток, инсайты."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        income = user.income

        expenses = Expense.objects.filter(user=user)

        # Общий расход
        total_expense = expenses.aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0')

        # Расход по категориям
        by_category = {}
        for category, label in Expense.CATEGORY_CHOICES:
            cat_sum = expenses.filter(category=category).aggregate(
                total=Sum('amount')
            )['total'] or Decimal('0')
            by_category[category] = {
                'label': label,
                'amount': cat_sum
            }

        # Остаток
        balance = income - total_expense

        # Накопления (прогресс по целям)
        total_saved = Goal.objects.filter(user=user).aggregate(
            total=Sum('current_amount')
        )['total'] or Decimal('0')

        # Инсайты
        insights = []

        food_amount = by_category.get('food', {}).get('amount', Decimal('0'))
        if income > 0 and food_amount > income * Decimal('0.5'):
            insights.append({
                'type': 'warning',
                'message': f'Ты тратишь слишком много на еду — '
                           f'{food_amount} из {income} '
                           f'({round(float(food_amount)/float(income)*100, 1)}% дохода).'
            })

        if total_saved == 0:
            insights.append({
                'type': 'warning',
                'message': 'У тебя нет накоплений. Попробуй создать финансовую цель и откладывать деньги.'
            })

        if balance < 0:
            insights.append({
                'type': 'danger',
                'message': f'Твои расходы превышают доход на {abs(balance)}. Срочно пересмотри бюджет.'
            })
        elif income > 0 and balance > income * Decimal('0.2'):
            insights.append({
                'type': 'success',
                'message': f'Отличная работа! Ты сохраняешь {balance} ({round(float(balance)/float(income)*100, 1)}% дохода).'
            })

        return Response({
            'income': income,
            'total_expense': total_expense,
            'balance': balance,
            'by_category': by_category,
            'total_saved': total_saved,
            'insights': insights,
        })