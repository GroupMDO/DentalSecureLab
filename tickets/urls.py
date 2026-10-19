
from django.urls import path
from . import views

app_name = "tickets"

urlpatterns = [
    path("", views.ticket_list, name="ticket_list"),
    path("nuevo/", views.ticket_create, name="ticket_create"),
    path("<int:pk>/", views.ticket_detail, name="ticket_detail"),
    path(
        "<int:pk>/estado/",
        views.ticket_change_status,
        name="ticket_change_status",
    ),
]
