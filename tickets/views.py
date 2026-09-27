from django.shortcuts import render, get_object_or_404
from .models import Ticket, Articulo
from .cola import ColaCircular

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

def lista_tickets(request):
    estado_filtro = request.GET.get('estado', 'Pendiente')
    
    # 1. Obtener tickets según el estado seleccionado (por defecto 'Pendiente')
    tickets_filtrados = Ticket.objects.filter(estado__iexact=estado_filtro)
    
    # 2. Inicializar la cola circular con la capacidad necesaria
    capacidad = len(tickets_filtrados) if len(tickets_filtrados) > 0 else 1
    cola = ColaCircular(capacidad)
    
    # 3. Encolar
    for ticket in tickets_filtrados:
        cola.encolar(ticket)
        
    # 4. Desencolar para determinar el orden estricto de atención
    tickets_ordenados = []
    ticket_actual = cola.desencolar()
    while ticket_actual is not None:
        tickets_ordenados.append(ticket_actual)
        ticket_actual = cola.desencolar()

    return render(request, 'tickets/lista.html', {
        'tickets': tickets_ordenados,
        'estado_actual': estado_filtro
    })

def detalle_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'tickets/detalle.html', {'ticket': ticket})
