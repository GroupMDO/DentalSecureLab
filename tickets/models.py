import re
import unicodedata
import uuid
from django.db import models


def normalizar_texto(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower()


class Ticket(models.Model):
    TIPOS = [
        ("Solicitud", "Solicitud"),
        ("Incidencia", "Incidencia"),
    ]

    PRIORIDADES = [
        ("Baja", "Baja"),
        ("Media", "Media"),
        ("Alta", "Alta"),
        ("Crítica", "Crítica"),
    ]

    AREAS = [
        ("Soporte", "Soporte"),
        ("Infraestructura", "Infraestructura"),
        ("Desarrollo", "Desarrollo"),
    ]

    ESTADOS = [
        ("Registrado", "Registrado"),
        ("En proceso", "En proceso"),
        ("Pendiente de usuario", "Pendiente de usuario"),
        ("Resuelto", "Resuelto"),
        ("Cerrado", "Cerrado"),
    ]

    folio = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
    )

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    solicitante = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )

    activo_afectado = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS,
        default="Solicitud",
    )

    prioridad = models.CharField(
        max_length=20,
        choices=PRIORIDADES,
        default="Media",
    )

    area_asignada = models.CharField(
        max_length=30,
        choices=AREAS,
        default="Soporte",
    )

    estado = models.CharField(
        max_length=30,
        choices=ESTADOS,
        default="Registrado",
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
    )

    def derivar_automaticamente(self):
        texto = normalizar_texto(f"{self.titulo} {self.descripcion}")

        palabras_infraestructura = [
            "servidor", "red", "internet",
            "wifi", "router", "conexion",
        ]

        palabras_desarrollo = [
            "software", "aplicacion", "sistema",
            "codigo", "programacion", "bug",
        ]

        def contiene_palabra(palabra, texto_fuente):
            return bool(re.search(rf"\b{re.escape(palabra)}\b", texto_fuente))

        if any(
            contiene_palabra(palabra, texto)
            for palabra in palabras_infraestructura
        ):
            self.area_asignada = "Infraestructura"

        elif any(
            contiene_palabra(palabra, texto)
            for palabra in palabras_desarrollo
        ):
            self.area_asignada = "Desarrollo"

        else:
            self.area_asignada = "Soporte"

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None

        if not self.folio:
            self.folio = f"TK-{uuid.uuid4().hex[:8].upper()}"

        if es_nuevo:
            self.derivar_automaticamente()

        super().save(*args, **kwargs)

        if es_nuevo:
            Alerta.objects.create(
                ticket=self,
                mensaje=f"Se creó el ticket {self.folio}",
            )

    def __str__(self):
        return self.folio


class Alerta(models.Model):
    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        related_name="alerta",
    )

    mensaje = models.CharField(
        max_length=255,
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.mensaje
