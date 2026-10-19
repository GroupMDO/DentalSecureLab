
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TicketForm
from .models import Ticket


@login_required
def ticket_list(request):
    tickets = Ticket.objects.all().order_by("-fecha_creacion")

    return render(
        request,
        "tickets/ticket_list.html",
        {"tickets": tickets},
    )


@login_required
def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(request.POST)

        if form.is_valid():
            ticket = form.save()
            return redirect("tickets:ticket_detail", pk=ticket.pk)
    else:
        form = TicketForm()

    return render(
        request,
        "tickets/ticket_form.html",
        {"form": form},
    )


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    return render(
        request,
        "tickets/ticket_detail.html",
        {
            "ticket": ticket,
            "estados": Ticket.ESTADOS,
        },
    )


@login_required
@require_POST
def ticket_change_status(request, pk):
    if not request.user.is_staff:
        return render(
            request,
            "403.html",
            {"exception": "No tienes permisos de personal autorizado para cambiar el estado del ticket."},
            status=403,
        )

    ticket = get_object_or_404(Ticket, pk=pk)
    nuevo_estado = request.POST.get("estado")

    estados_validos = [
        valor for valor, etiqueta in Ticket.ESTADOS
    ]

    if nuevo_estado not in estados_validos:
        return render(
            request,
            "403.html",
            {"exception": "El estado seleccionado no es válido."},
            status=403,
        )

    ticket.estado = nuevo_estado
    ticket.save(update_fields=["estado"])

    return redirect("tickets:ticket_detail", pk=ticket.pk)

