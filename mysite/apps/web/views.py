"""
apps/web/views.py — HTML-шаблонные вьюхи для AkchaAI
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal

from apps.users.models import User
from apps.finance.models import Expense
from apps.goals.models import Goal


# ─── AUTH ────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Неверный логин или пароль.')
    return render(request, 'akchaai/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    from apps.users.serializers import RegisterSerializer  # reuse validation
    errors = {}
    if request.method == 'POST':
        p = request.POST
        if p.get('password') != p.get('password2'):
            errors['password'] = ['Пароли не совпадают.']
        else:
            try:
                user = User.objects.create_user(
                    username=p.get('username', '').strip(),
                    email=p.get('email', '').strip(),
                    password=p.get('password'),
                )
                income = p.get('income', '0') or '0'
                user.income = Decimal(income)
                user.save()
                login(request, user)
                return redirect('dashboard')
            except Exception as e:
                errors['general'] = [str(e)]

    return render(request, 'akchaai/register.html', {'form': type('F', (), {'errors': errors, 'username': type('F2',(),{'errors':errors.get('username',[])})(), 'password': type('F2',(),{'errors':errors.get('password',[])})()})()})


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── HELPERS ─────────────────────────────────────────────────────────────────

def _get_stats(user):
    income = user.income
    expenses = Expense.objects.filter(user=user)
    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0')

    by_category = {}
    for category, label in Expense.CATEGORY_CHOICES:
        cat_sum = expenses.filter(category=category).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        by_category[category] = {'label': label, 'amount': cat_sum}

    balance = income - total_expense
    total_saved = Goal.objects.filter(user=user).aggregate(total=Sum('current_amount'))['total'] or Decimal('0')

    insights = []
    food_amount = by_category.get('food', {}).get('amount', Decimal('0'))
    if income > 0 and food_amount > income * Decimal('0.5'):
        insights.append({'type': 'warning', 'message': f'Ты тратишь слишком много на еду — {food_amount} из {income} ({round(float(food_amount)/float(income)*100,1)}% дохода).'})
    if total_saved == 0:
        insights.append({'type': 'warning', 'message': 'У тебя нет накоплений. Попробуй создать финансовую цель.'})
    if balance < 0:
        insights.append({'type': 'danger', 'message': f'Твои расходы превышают доход на {abs(balance)} сом. Срочно пересмотри бюджет.'})
    elif income > 0 and balance > income * Decimal('0.2'):
        insights.append({'type': 'success', 'message': f'Отличная работа! Ты сохраняешь {balance} сом ({round(float(balance)/float(income)*100,1)}% дохода).'})

    return {
        'income': income,
        'total_expense': total_expense,
        'balance': balance,
        'by_category': by_category,
        'total_saved': total_saved,
        'insights': insights,
    }


# ─── DASHBOARD ───────────────────────────────────────────────────────────────

@login_required
def dashboard_view(request):
    stats = _get_stats(request.user)
    recent_expenses = Expense.objects.filter(user=request.user)[:6]
    goals = Goal.objects.filter(user=request.user)[:4]
    return render(request, 'akchaai/dashboard.html', {
        'stats': stats,
        'recent_expenses': recent_expenses,
        'goals': goals,
    })


# ─── EXPENSES ────────────────────────────────────────────────────────────────

@login_required
def expenses_view(request):
    qs = Expense.objects.filter(user=request.user)
    category = request.GET.get('category')
    date = request.GET.get('date')
    if category:
        qs = qs.filter(category=category)
    if date:
        qs = qs.filter(date=date)
    return render(request, 'akchaai/expenses.html', {'expenses': qs})


@login_required
def expense_create_view(request):
    if request.method == 'POST':
        p = request.POST
        try:
            Expense.objects.create(
                user=request.user,
                title=p.get('title', '').strip(),
                amount=Decimal(p.get('amount', '0')),
                category=p.get('category', 'other'),
                note=p.get('note', '').strip(),
            )
            messages.success(request, 'Расход добавлен.')
        except Exception as e:
            messages.error(request, f'Ошибка: {e}')
    return redirect('expenses')


@login_required
def expense_delete_view(request, pk):
    exp = get_object_or_404(Expense, pk=pk, user=request.user)
    exp.delete()
    messages.success(request, 'Расход удалён.')
    return redirect('expenses')


# ─── GOALS ───────────────────────────────────────────────────────────────────

@login_required
def goals_view(request):
    goals = Goal.objects.filter(user=request.user)
    return render(request, 'akchaai/goals.html', {'goals': goals})


@login_required
def goal_create_view(request):
    if request.method == 'POST':
        p = request.POST
        try:
            Goal.objects.create(
                user=request.user,
                title=p.get('title', '').strip(),
                target_amount=Decimal(p.get('target_amount', '1')),
                current_amount=Decimal(p.get('current_amount', '0') or '0'),
                deadline=p.get('deadline') or None,
            )
            messages.success(request, 'Цель создана.')
        except Exception as e:
            messages.error(request, f'Ошибка: {e}')
    return redirect('goals')


@login_required
def goal_deposit_view(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
            if amount > 0:
                goal.current_amount += amount
                goal.save()
                messages.success(request, f'Пополнено на {amount} сом.')
        except Exception as e:
            messages.error(request, f'Ошибка: {e}')
    return redirect('goals')


@login_required
def goal_delete_view(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    goal.delete()
    messages.success(request, 'Цель удалена.')
    return redirect('goals')


# ─── ANALYTICS ───────────────────────────────────────────────────────────────

@login_required
def analytics_view(request):
    stats = _get_stats(request.user)
    return render(request, 'akchaai/analytics.html', {'stats': stats})


# ─── PROFILE ─────────────────────────────────────────────────────────────────

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        p = request.POST
        user.email = p.get('email', '').strip()
        user.income = Decimal(p.get('income', '0') or '0')
        user.save()
        messages.success(request, 'Профиль обновлён.')
        return redirect('profile')

    expense_count = Expense.objects.filter(user=user).count()
    goal_count = Goal.objects.filter(user=user).count()
    return render(request, 'akchaai/profile.html', {
        'expense_count': expense_count,
        'goal_count': goal_count,
    })