from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Patient


class PatientSecurityAccessTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="doctor_test",
            password="Password123!"
        )
        self.patient = Patient.objects.create(
            first_name="Carlos",
            last_name="Gomez",
            birth_date="1990-01-01",
            email="carlos@example.com",
            phone="5551234567",
        )

    def test_listado_pacientes_requiere_autenticacion(self):
        response = self.client.get(reverse("patient_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/usuarios/login/", response.url)

    def test_crear_paciente_requiere_autenticacion(self):
        response = self.client.get(reverse("patient_create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/usuarios/login/", response.url)

    def test_detalle_paciente_requiere_autenticacion(self):
        response = self.client.get(reverse("patient_detail", args=[self.patient.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/usuarios/login/", response.url)

    def test_editar_paciente_requiere_autenticacion(self):
        response = self.client.get(reverse("patient_update", args=[self.patient.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/usuarios/login/", response.url)

    def test_eliminar_paciente_requiere_autenticacion(self):
        response = self.client.get(reverse("patient_delete", args=[self.patient.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/usuarios/login/", response.url)

    def test_usuario_autenticado_puede_ver_pacientes(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("patient_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Carlos")
