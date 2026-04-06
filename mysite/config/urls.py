from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/expenses/', include('apps.finance.urls')),
    path('api/goals/', include('apps.goals.urls')),
    path('api/stats/', include('apps.analytics.urls')),
]