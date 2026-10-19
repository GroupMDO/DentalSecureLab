
from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "titulo",
            "descripcion",
            "solicitante",
            "activo_afectado",
            "tipo",
            "prioridad",
        ]

        widgets = {
            "descripcion": forms.Textarea(
                attrs={"rows": 4}
            ),
        }
