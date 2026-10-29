from django.contrib import admin
from .models import Ticket, Usuario, Articulo, Categoria, Comentario

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("titulo", "estado", "impacto", "categoria", "propietario", "agente_asignado", "formula_postfija")
    list_filter = ("estado", "impacto", "categoria")

admin.site.register(Usuario)
admin.site.register(Articulo)
admin.site.register(Categoria)
admin.site.register(Comentario)