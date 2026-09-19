from .estructura import Pila, Cola
from .models import Ticket

cola_tickets = Cola()
historiales = {}  # id del ticket -> Pila con sus estados anteriores


def crear_ticket(titulo, descripcion):
    """Crea el ticket y lo encola."""
    ticket = Ticket.objects.create(titulo=titulo, descripcion=descripcion)
    cola_tickets.enqueue(ticket)
    return ticket


def cambiar_estado(ticket, nuevo_estado):
    """Apila el estado anterior antes de asignar el nuevo estado."""
    historiales.setdefault(ticket.pk, Pila()).push(ticket.estado)
    ticket.estado = nuevo_estado
    ticket.save()


def deshacer_ultimo_cambio(ticket):
    """Usa pop() sobre la pila para devolver el ticket a su estado anterior."""
    historial = historiales.get(ticket.pk)
    estado_anterior = historial.pop() if historial else None
    if estado_anterior is None:
        print("No hay estados anteriores para deshacer.")
        return False
    ticket.estado = estado_anterior
    ticket.save()
    return True


def asignar_siguiente_ticket(agente):
    """Usa dequeue() para obtener el ticket más antiguo y asignarlo al agente."""
    ticket = cola_tickets.dequeue()
    if ticket is None:
        return None
    ticket.agente_asignado = agente
    cambiar_estado(ticket, "En progreso")
    return ticket
