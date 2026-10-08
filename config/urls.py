"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include
from core.views import dashboard
from users.views import LoginSeguroView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Inicio de sesión
    path(
        'login/',
        LoginSeguroView.as_view(),
        name='login'
    ),

    path('', dashboard, name='dashboard'),
    path('pacientes/', include('patients.urls')),
    path('agenda/', include('agenda.urls')),
    path('expedientes/', include('records.urls')),
    path('pagos/', include('payments.urls')),
]