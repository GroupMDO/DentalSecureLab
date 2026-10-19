from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group


class RecordsAccessControlTest(TestCase):

    def setUp(self):
        self.usuario_anonimo = None

        self.user_soporte = User.objects.create_user(
            username="soporte_test",
            password="Password123!",
        )
        grupo_soporte = Group.objects.create(name="Soporte")
        self.user_soporte.groups.add(grupo_soporte)

        self.user_recepcion = User.objects.create_user(
            username="recepcion_test",
            password="Password123!",
        )
        grupo_recepcion = Group.objects.create(name="Recepción")
        self.user_recepcion.groups.add(grupo_recepcion)

        self.user_admin = User.objects.create_user(
            username="admin_test",
            password="Password123!",
        )
        grupo_admin = Group.objects.create(name="Administrador")
        self.user_admin.groups.add(grupo_admin)

    def test_expedientes_requiere_autenticacion(self):
        respuesta = self.client.get(reverse("record_list"))
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn("/usuarios/login/", respuesta.url)

    def test_usuario_soporte_bloqueado_en_expedientes_con_interfaz_informativa(self):
        self.client.force_login(self.user_soporte)
        respuesta = self.client.get(reverse("record_list"))
        self.assertEqual(respuesta.status_code, 403)
        self.assertContains(respuesta, "Acceso Restringido: Expedientes Clínicos", status_code=403)
        self.assertContains(respuesta, "Soporte TI", status_code=403)
        self.assertContains(respuesta, "Tickets TI", status_code=403)

    def test_usuario_recepcion_bloqueado_en_expedientes_con_interfaz_informativa(self):
        self.client.force_login(self.user_recepcion)
        respuesta = self.client.get(reverse("record_list"))
        self.assertEqual(respuesta.status_code, 403)
        self.assertContains(respuesta, "Acceso Restringido: Expedientes Clínicos", status_code=403)
        self.assertContains(respuesta, "Recepción", status_code=403)
        self.assertContains(respuesta, "Pacientes", status_code=403)

    def test_usuario_administrador_puede_acceder_expedientes(self):
        self.client.force_login(self.user_admin)
        respuesta = self.client.get(reverse("record_list"))
        self.assertEqual(respuesta.status_code, 200)
