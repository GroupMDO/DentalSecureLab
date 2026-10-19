from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from patients.models import Patient
from .models import Appointment


class AgendaSecurityAccessTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="recepcion_test",
            password="Password123!"
        )
        self.patient = Patient.objects.create(
            first_name="Laura",
            last_name="Mendez",
            birth_date="1990-01-01",
            email="laura@example.com",
            phone="5559876543",
        )
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            date=timezone.localdate(),
            time="10:00:00",
            reason="Limpieza dental",
            status="scheduled",
        )

    def test_listado_citas_requiere_autenticacion(self):
        response = self.client.get(reverse("appointment_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/usuarios/login/", response.url)

    def test_crear_cita_requiere_autenticacion(self):
        response = self.client.get(reverse("appointment_create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/usuarios/login/", response.url)

    def test_editar_cita_requiere_autenticacion(self):
        response = self.client.get(reverse("appointment_update", args=[self.appointment.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/usuarios/login/", response.url)

    def test_usuario_autenticado_puede_ver_agenda(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("appointment_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Limpieza dental")
