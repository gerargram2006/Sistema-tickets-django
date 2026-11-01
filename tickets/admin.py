from django.contrib import admin
from .models import Ticket, Usuario, Articulo, Categoria, Comentario

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "peso", "padre")

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("titulo", "estado", "impacto", "categoria", "creado_por", "creado")
    list_filter = ("estado", "impacto", "categoria")

admin.site.register(Usuario)
admin.site.register(Articulo)
admin.site.register(Comentario)