
"""
URL configuration for DentalSecureLab.
"""

from django.contrib import admin
from django.urls import path, include
from core.views import dashboard


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', dashboard, name='dashboard'),

    path('pacientes/', include('patients.urls')),

    path('agenda/', include('agenda.urls')),

    path('expedientes/', include('records.urls')),

    path('pagos/', include('payments.urls')),

    path('usuarios/', include('users.urls')),

    path('tickets/', include('tickets.urls')),
]

handler403 = 'core.views.custom_403_view'

