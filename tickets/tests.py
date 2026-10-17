from django.test import TestCase
from .models import Ticket, Alerta


class TicketTest(TestCase):

    def test_ticket_genera_folio_automaticamente(self):
        ticket = Ticket.objects.create(
            titulo="Error de acceso",
            descripcion="El usuario no puede acceder al sistema"
        )

        self.assertIsNotNone(ticket.folio)
        self.assertNotEqual(ticket.folio, "")

    def test_folios_de_tickets_son_unicos(self):
        ticket1 = Ticket.objects.create(
            titulo="Primer ticket",
            descripcion="Descripción del primer ticket"
        )

        ticket2 = Ticket.objects.create(
            titulo="Segundo ticket",
            descripcion="Descripción del segundo ticket"
        )

        self.assertNotEqual(
            ticket1.folio,
            ticket2.folio
        )

    def test_crear_ticket_genera_alerta(self):
        ticket = Ticket.objects.create(
            titulo="Problema en expediente",
            descripcion="No se puede consultar el expediente"
        )

        self.assertTrue(
            Alerta.objects.filter(
                ticket=ticket
            ).exists()
        )