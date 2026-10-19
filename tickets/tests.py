
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Ticket, Alerta


class TicketTest(TestCase):

    def test_ticket_genera_folio_automaticamente(self):
        ticket = Ticket.objects.create(
            titulo="Error de acceso",
            descripcion="El usuario no puede acceder al sistema",
        )

        self.assertTrue(ticket.folio.startswith("TK-"))

    def test_folios_de_tickets_son_unicos(self):
        ticket1 = Ticket.objects.create(
            titulo="Primer ticket",
            descripcion="Descripción del primer ticket",
        )

        ticket2 = Ticket.objects.create(
            titulo="Segundo ticket",
            descripcion="Descripción del segundo ticket",
        )

        self.assertNotEqual(ticket1.folio, ticket2.folio)

    def test_crear_ticket_genera_alerta(self):
        ticket = Ticket.objects.create(
            titulo="Problema en expediente",
            descripcion="No se puede consultar el expediente",
        )

        self.assertTrue(
            Alerta.objects.filter(ticket=ticket).exists()
        )

    def test_derivacion_a_infraestructura(self):
        ticket = Ticket.objects.create(
            titulo="Falla de servidor",
            descripcion="El servidor no responde",
        )

        self.assertEqual(
            ticket.area_asignada,
            "Infraestructura",
        )

    def test_derivacion_a_desarrollo(self):
        ticket = Ticket.objects.create(
            titulo="Error de software",
            descripcion="La aplicación presenta un bug",
        )

        self.assertEqual(
            ticket.area_asignada,
            "Desarrollo",
        )

    def test_derivacion_a_soporte(self):
        ticket = Ticket.objects.create(
            titulo="Problema con impresora",
            descripcion="No imprime correctamente",
        )

        self.assertEqual(ticket.area_asignada, "Soporte")

    def test_estado_inicial_registrado(self):
        ticket = Ticket.objects.create(
            titulo="Solicitud de ayuda",
            descripcion="Necesito asistencia",
        )

        self.assertEqual(ticket.estado, "Registrado")

    def test_actualizar_estado_no_genera_otra_alerta(self):
        ticket = Ticket.objects.create(
            titulo="Solicitud de ayuda",
            descripcion="Necesito asistencia",
        )

        ticket.estado = "En proceso"
        ticket.save(update_fields=["estado"])

        self.assertEqual(
            Alerta.objects.filter(ticket=ticket).count(),
            1,
        )


class TicketViewTest(TestCase):

    def setUp(self):
        User = get_user_model()

        self.usuario = User.objects.create_user(
            username="usuario_prueba",
            password="ClaveSegura123!",
        )

        self.staff = User.objects.create_user(
            username="staff_prueba",
            password="ClaveSegura123!",
            is_staff=True,
        )

        self.ticket = Ticket.objects.create(
            titulo="Problema con impresora",
            descripcion="No imprime correctamente",
        )

    def test_listado_requiere_autenticacion(self):
        respuesta = self.client.get(
            reverse("tickets:ticket_list")
        )

        self.assertEqual(respuesta.status_code, 302)

    def test_usuario_autenticado_puede_ver_listado(self):
        self.client.force_login(self.usuario)

        respuesta = self.client.get(
            reverse("tickets:ticket_list")
        )

        self.assertEqual(respuesta.status_code, 200)

    def test_usuario_no_staff_no_cambia_estado(self):
        self.client.force_login(self.usuario)

        respuesta = self.client.post(
            reverse(
                "tickets:ticket_change_status",
                args=[self.ticket.pk],
            ),
            {"estado": "Resuelto"},
        )

        self.assertEqual(respuesta.status_code, 403)

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.estado, "Registrado")

    def test_staff_puede_cambiar_estado(self):
        self.client.force_login(self.staff)

        respuesta = self.client.post(
            reverse(
                "tickets:ticket_change_status",
                args=[self.ticket.pk],
            ),
            {"estado": "Resuelto"},
        )

        self.assertEqual(respuesta.status_code, 302)

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.estado, "Resuelto")

    def test_estado_invalido_es_rechazado(self):
        self.client.force_login(self.staff)

        respuesta = self.client.post(
            reverse(
                "tickets:ticket_change_status",
                args=[self.ticket.pk],
            ),
            {"estado": "Estado inventado"},
        )

        self.assertEqual(respuesta.status_code, 403)

        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.estado, "Registrado")
