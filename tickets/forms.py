from django import forms
from .models import Ticket, Usuario


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["titulo", "descripcion", "categoria", "agente_asignado"]
        labels = {
            "categoria": "Categoría",
            "agente_asignado": "Agente encargado",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["agente_asignado"].queryset = Usuario.objects.order_by("nombre")
        self.fields["agente_asignado"].empty_label = "Sin asignar"
