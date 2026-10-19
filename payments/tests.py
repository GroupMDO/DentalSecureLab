from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from patients.models import Patient
from .models import Payment


class PaymentSecurityAccessTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="doctor_caja",
            password="Password123!"
        )
        self.patient = Patient.objects.create(
            first_name="Roberto",
            last_name="Sanchez",
            birth_date="1990-01-01",
            email="roberto@example.com",
            phone="5553334444",
        )
        self.payment = Payment.objects.create(
            patient=self.patient,
            date=timezone.localdate(),
            concept="Consulta de valoración",
            amount=500.00,
            payment_method="cash",
        )

    def test_listado_pagos_requiere_autenticacion(self):
        response = self.client.get(reverse("payment_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/usuarios/login/", response.url)

    def test_crear_pago_requiere_autenticacion(self):
        response = self.client.get(reverse("payment_create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/usuarios/login/", response.url)

    def test_editar_pago_requiere_autenticacion(self):
        response = self.client.get(reverse("payment_update", args=[self.payment.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/usuarios/login/", response.url)

    def test_usuario_autenticado_puede_ver_pagos(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("payment_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Consulta de valoración")
