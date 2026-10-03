from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Ticket, Usuario


class TicketAgentAssignmentTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Software")
        self.agente = Usuario.objects.create(
            nombre="Ana Agente",
            email="ana@example.com",
        )

    def test_new_ticket_form_lists_agents_and_assigns_selected_agent(self):
        response = self.client.get(reverse("crear_ticket_form"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ana Agente")

        response = self.client.post(
            reverse("crear_ticket_form"),
            {
                "titulo": "No inicia el sistema",
                "descripcion": "Error al iniciar la aplicación",
                "categoria": self.categoria.pk,
                "agente_asignado": self.agente.pk,
            },
        )

        self.assertRedirects(response, reverse("lista_tickets"))
        ticket = Ticket.objects.get(titulo="No inicia el sistema")
        self.assertEqual(ticket.agente_asignado, self.agente)

    def test_ticket_can_be_reassigned_or_unassigned(self):
        nuevo_agente = Usuario.objects.create(
            nombre="Luis Agente",
            email="luis@example.com",
        )
        ticket = Ticket.objects.create(
            titulo="Impresora sin conexión",
            descripcion="La impresora no responde",
            categoria=self.categoria,
            agente_asignado=self.agente,
        )

        response = self.client.post(
            reverse("editar_ticket_form", args=[ticket.pk]),
            {
                "titulo": ticket.titulo,
                "descripcion": ticket.descripcion,
                "categoria": self.categoria.pk,
                "agente_asignado": nuevo_agente.pk,
            },
        )

        self.assertRedirects(
            response,
            reverse("detalle_ticket", args=[ticket.pk]),
        )
        ticket.refresh_from_db()
        self.assertEqual(ticket.agente_asignado, nuevo_agente)

        response = self.client.post(
            reverse("editar_ticket_form", args=[ticket.pk]),
            {
                "titulo": ticket.titulo,
                "descripcion": ticket.descripcion,
                "categoria": self.categoria.pk,
                "agente_asignado": "",
            },
        )

        self.assertRedirects(
            response,
            reverse("detalle_ticket", args=[ticket.pk]),
        )
        ticket.refresh_from_db()
        self.assertIsNone(ticket.agente_asignado)
