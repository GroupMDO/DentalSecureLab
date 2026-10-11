from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group


class LoginTest(TestCase):

    def test_pagina_login_existe(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)

    def test_usuario_con_credenciales_validas_inicia_sesion(self):
        User.objects.create_user(
            username="usuario_prueba",
            password="Prueba123!"
        )

        response = self.client.post(
            reverse("login"),
            {
                "username": "usuario_prueba",
                "password": "Prueba123!"
            }
        )

        self.assertTrue(
            response.wsgi_request.user.is_authenticated
        )

    def test_credenciales_invalidas_muestran_error(self):
        User.objects.create_user(
            username="usuario_prueba",
            password="Prueba123!"
        )

        response = self.client.post(
            reverse("login"),
            {
                "username": "usuario_prueba",
                "password": "Incorrecta123!"
            }
        )

        self.assertContains(
            response,
            "Usuario o contraseña incorrectos"
        )

    def test_usuario_sin_sesion_no_accede_dashboard(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/usuarios/login/", response.url)

    def test_usuario_puede_tener_rol_administrador(self):
        usuario = User.objects.create_user(
            username="admin_prueba",
            password="Prueba123!"
        )

        grupo = Group.objects.create(
            name="Administrador"
        )

        usuario.groups.add(grupo)

        self.assertTrue(
            usuario.groups.filter(
                name="Administrador"
            ).exists()
        )

    def test_usuario_soporte_no_accede_expedientes(self):
        usuario = User.objects.create_user(
            username="soporte_prueba",
            password="Prueba123!"
        )

        grupo = Group.objects.create(
            name="Soporte"
        )

        usuario.groups.add(grupo)

        self.client.login(
            username="soporte_prueba",
            password="Prueba123!"
        )

        response = self.client.get(
            reverse("record_list")
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_usuario_administrador_si_accede_expedientes(self):
        usuario = User.objects.create_user(
            username="admin_acceso",
            password="Prueba123!"
        )

        grupo = Group.objects.create(
            name="Administrador"
        )

        usuario.groups.add(grupo)

        self.client.login(
            username="admin_acceso",
            password="Prueba123!"
        )

        response = self.client.get(
            reverse("record_list")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_usuario_operador_si_accede_expedientes(self):
        usuario = User.objects.create_user(
            username="operador_prueba",
            password="Prueba123!"
        )

        grupo = Group.objects.create(
            name="Operador"
        )

        usuario.groups.add(grupo)

        self.client.login(
            username="operador_prueba",
            password="Prueba123!"
        )

        response = self.client.get(
            reverse("record_list")
        )

        self.assertEqual(
            response.status_code,
            200
        )