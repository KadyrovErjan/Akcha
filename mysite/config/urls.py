from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # REST API
    path('api/auth/',     include('apps.users.urls')),
    path('api/expenses/', include('apps.finance.urls')),
    path('api/goals/',    include('apps.goals.urls')),
    path('api/stats/',    include('apps.analytics.urls')),

    # HTML Web Interface  ← добавить
    path('', include('apps.web.urls')),
]