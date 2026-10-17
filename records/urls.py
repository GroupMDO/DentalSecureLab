from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_expedientes, name='record_list'),
]