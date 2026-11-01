from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Articulo
from .forms import TicketForm
from .historial import HistorialComentarios

def buscar_articulo(titulo_buscado):
    # Se obtienen todos los artículos y se ordenan alfabéticamente
    articulos = list(Articulo.objects.all().order_by('titulo'))
    inicio = 0
    fin = len(articulos) - 1
    comparaciones = 0

    while inicio <= fin:
        comparaciones += 1
        medio = (inicio + fin) // 2
        titulo_medio = articulos[medio].titulo

        if titulo_medio == titulo_buscado:
            return articulos[medio], comparaciones
        elif titulo_medio < titulo_buscado:
            inicio = medio + 1
        else:
            fin = medio - 1

    return None, comparaciones

@login_required
def lista_tickets(request):
    es_agente = request.user.groups.filter(name="Agente").exists() or request.user.is_superuser

    if es_agente:
        # El filtro Q es un árbol de expresión: AND es la raíz; Q(estado) es
        # la hoja izquierda y el OR de impacto/peso es el hijo derecho.
        filtro = Q(estado="abierto") & (Q(impacto__gte=4) | Q(categoria__peso__gte=3))
        tickets = list(Ticket.objects.filter(filtro))
        tickets.sort(key=lambda t: t.prioridad(), reverse=True)
    else:
        tickets = Ticket.objects.filter(creado_por=request.user)
        estado_filtro = request.GET.get("estado")
        if estado_filtro in dict(Ticket.ESTADOS):
            tickets = tickets.filter(estado=estado_filtro)

    return render(request, "tickets/lista.html", {
        "tickets": tickets,
        "es_agente": es_agente,
        "estado_actual": request.GET.get("estado", "abierto"),
    })

@login_required
def detalle_ticket(request, ticket_id):
    es_agente = request.user.groups.filter(name="Agente").exists() or request.user.is_superuser
    if es_agente:
        ticket = get_object_or_404(Ticket, id=ticket_id)
    else:
        ticket = get_object_or_404(Ticket, id=ticket_id, creado_por=request.user)
    comentarios = ticket.comentarios.order_by("fecha")

    historial = HistorialComentarios(comentarios)
    pos = int(request.GET.get("pos", 0))
    for _ in range(pos):
        historial.siguiente()

    return render(request, "tickets/detalle.html", {
        "ticket": ticket,
        "comentario_actual": historial.actual(),
        "hay_anterior": historial.hay_anterior(),
        "hay_siguiente": historial.hay_siguiente(),
        "pos": pos,
    })

@login_required
def crear_ticket_form(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.creado_por = request.user
            ticket.save()
            return redirect("lista_tickets")
    else:
        form = TicketForm()
    return render(request, "tickets/form_ticket.html", {"form": form, "titulo_pagina": "Nuevo ticket"})


@login_required
def editar_ticket_form(request, ticket_id):
    es_agente = request.user.groups.filter(name="Agente").exists() or request.user.is_superuser
    if es_agente:
        ticket = get_object_or_404(Ticket, id=ticket_id)
    else:
        ticket = get_object_or_404(Ticket, id=ticket_id, creado_por=request.user)
    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("detalle_ticket", ticket_id=ticket.id)
    else:
        form = TicketForm(instance=ticket)
    return render(request, "tickets/form_ticket.html", {"form": form, "titulo_pagina": "Editar ticket"})
