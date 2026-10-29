from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Articulo
from .cola import ColaCircular
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
    if request.user.is_staff:
        filtro = Q(estado="abierto") & (Q(impacto__gte=4))
        tickets = Ticket.objects.filter(filtro)
        tickets_ordenados = sorted(tickets, key=lambda ticket: ticket.prioridad(), reverse=True)
        modo = "urgentes"
    else:
        estado_filtro = request.GET.get("estado", "abierto")
        tickets = Ticket.objects.filter(propietario=request.user)
        if estado_filtro in dict(Ticket.ESTADOS):
            tickets = tickets.filter(estado=estado_filtro)
        capacidad = len(tickets) if tickets else 1
        cola = ColaCircular(capacidad)
        for ticket in tickets:
            cola.encolar(ticket)
        tickets_ordenados = []
        ticket_actual = cola.desencolar()
        while ticket_actual is not None:
            tickets_ordenados.append(ticket_actual)
            ticket_actual = cola.desencolar()
        modo = "cliente"

    return render(request, 'tickets/lista.html', {
        'tickets': tickets_ordenados,
        'estado_actual': request.GET.get("estado", "abierto"),
        'modo': modo,
    })

@login_required
def detalle_ticket(request, ticket_id):
    if request.user.is_staff:
        ticket = get_object_or_404(Ticket, id=ticket_id)
    else:
        ticket = get_object_or_404(Ticket, id=ticket_id, propietario=request.user)
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
            ticket.propietario = request.user
            ticket.save()
            return redirect("lista_tickets")
    else:
        form = TicketForm()
    return render(request, "tickets/form_ticket.html", {"form": form, "titulo_pagina": "Nuevo ticket"})


@login_required
def editar_ticket_form(request, ticket_id):
    if request.user.is_staff:
        ticket = get_object_or_404(Ticket, id=ticket_id)
    else:
        ticket = get_object_or_404(Ticket, id=ticket_id, propietario=request.user)
    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("detalle_ticket", ticket_id=ticket.id)
    else:
        form = TicketForm(instance=ticket)
    return render(request, "tickets/form_ticket.html", {"form": form, "titulo_pagina": "Editar ticket"})
