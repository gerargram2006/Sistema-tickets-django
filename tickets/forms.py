from django import forms
from .models import Ticket, Usuario


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["titulo", "descripcion", "categoria", "impacto", "estado", "agente_asignado"]
        labels = {
            "categoria": "Categoría",
            "impacto": "Impacto (1-5)",
            "agente_asignado": "Agente encargado",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["impacto"].required = False
        self.fields["impacto"].initial = 1
        self.fields["impacto"].widget.attrs.update({"min": 1, "max": 5})
        self.fields["estado"].required = False
        self.fields["estado"].initial = "abierto"
        self.fields["agente_asignado"].queryset = Usuario.objects.order_by("nombre")
        self.fields["agente_asignado"].empty_label = "Sin asignar"

    def clean_impacto(self):
        impacto = self.cleaned_data.get("impacto") or 1
        if impacto < 1 or impacto > 5:
            raise forms.ValidationError("El impacto debe estar entre 1 y 5.")
        return impacto

    def clean_estado(self):
        return self.cleaned_data.get("estado") or "abierto"
