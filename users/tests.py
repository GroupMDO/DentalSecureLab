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

    def test_bloqueo_fuerza_bruta_tras_cinco_intentos_fallidos(self):
        from django.core.cache import cache
        cache.clear()

        User.objects.create_user(
            username="victima_bruteforce",
            password="PasswordValido123!"
        )

        for _ in range(4):
            r = self.client.post(
                reverse("login"),
                {"username": "victima_bruteforce", "password": "PasswordErroneo!"}
            )
            self.assertEqual(r.status_code, 200)
            self.assertContains(r, "Usuario o contraseña incorrectos")

        r5 = self.client.post(
            reverse("login"),
            {"username": "victima_bruteforce", "password": "PasswordErroneo!"}
        )
        self.assertEqual(r5.status_code, 403)
        self.assertContains(r5, "Cuenta bloqueada temporalmente por acumular 5 intentos fallidos", status_code=403)

        r6 = self.client.post(
            reverse("login"),
            {"username": "victima_bruteforce", "password": "PasswordValido123!"}
        )
        self.assertEqual(r6.status_code, 403)
        self.assertContains(r6, "Cuenta bloqueada temporalmente", status_code=403)

    def test_login_exitoso_restablece_contador_de_intentos(self):
        from django.core.cache import cache
        cache.clear()

        User.objects.create_user(
            username="usuario_recuperado",
            password="PasswordValido123!"
        )

        for _ in range(2):
            self.client.post(
                reverse("login"),
                {"username": "usuario_recuperado", "password": "Erroneo!"}
            )

        r_ok = self.client.post(
            reverse("login"),
            {"username": "usuario_recuperado", "password": "PasswordValido123!"}
        )
        self.assertEqual(r_ok.status_code, 302)
        self.assertIsNone(cache.get("login_attempts_usuario_recuperado"))

    # Control de seguridad: Verificación de destrucción de sesión en logout (OWASP ASVS V3.3)
    # Contribución técnica de QA: Pamela Vicario Lara (QA / Testing y Dependencias)
    def test_logout_cierra_sesion_exitosamente(self):
        """
        Verifica que al invocar la vista de cierre de sesión (logout),
        la sesión del usuario sea destruida inmediatamente y que
        solicitudes subsiguientes a rutas protegidas (ej. dashboard)
        sean redirigidas al formulario de login (HTTP 302).
        Control OWASP ASVS v4.0.3 Nivel 2 - Requisito V3.3.
        """
        usuario = User.objects.create_user(
            username="logout_prueba",
            password="Prueba123!",
        )

        self.client.force_login(usuario)

        respuesta = self.client.post(reverse("logout"))

        self.assertEqual(respuesta.status_code, 302)
        self.assertFalse(
            respuesta.wsgi_request.user.is_authenticated
        )

        respuesta_dashboard = self.client.get(reverse("dashboard"))
        self.assertEqual(respuesta_dashboard.status_code, 302)
        self.assertIn("/usuarios/login/", respuesta_dashboard.url)
