from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Ticket
from .cola import crear_ticket


def demo_fifo(request):
    crear_ticket("Ticket de prueba 1", "Primero")
    messages.success(request, "Ticket 1 creado")
    crear_ticket("Ticket de prueba 2", "Segundo")
    messages.success(request, "Ticket 2 creado")
    return redirect("lista_tickets")


def lista_tickets(request):
    return render(request, "tickets/lista.html", {"tickets": Ticket.objects.all()})
