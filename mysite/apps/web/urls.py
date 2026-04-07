"""
apps/web/urls.py — URL-паттерны для HTML-интерфейса
"""
from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/',    views.login_view,    name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/',   views.logout_view,   name='logout'),

    # Main pages
    path('',            views.dashboard_view,  name='dashboard'),
    path('expenses/',   views.expenses_view,   name='expenses'),
    path('goals/',      views.goals_view,      name='goals'),
    path('analytics/',  views.analytics_view,  name='analytics'),
    path('profile/',    views.profile_view,     name='profile'),

    # Actions
    path('expenses/create/',       views.expense_create_view, name='expense_create'),
    path('expenses/<int:pk>/delete/', views.expense_delete_view, name='expense_delete'),
    path('goals/create/',          views.goal_create_view,    name='goal_create'),
    path('goals/<int:pk>/deposit/', views.goal_deposit_view,  name='goal_deposit'),
    path('goals/<int:pk>/delete/', views.goal_delete_view,   name='goal_delete'),
]