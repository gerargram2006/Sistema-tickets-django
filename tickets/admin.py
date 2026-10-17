from django.contrib import admin
from .models import Ticket, Usuario, Articulo, Categoria, Comentario

admin.site.register(Ticket)
admin.site.register(Usuario)
admin.site.register(Articulo)
admin.site.register(Categoria)
admin.site.register(Comentario)