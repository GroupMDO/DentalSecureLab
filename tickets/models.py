from django.db import models
import uuid


class Ticket(models.Model):
    folio = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    titulo = models.CharField(
        max_length=200
    )

    descripcion = models.TextField()

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None

        if not self.folio:
            self.folio = f"TK-{uuid.uuid4().hex[:8].upper()}"

        super().save(*args, **kwargs)

        if es_nuevo:
            Alerta.objects.create(
                ticket=self,
                mensaje=f"Se creó el ticket {self.folio}"
            )

    def __str__(self):
        return self.folio


class Alerta(models.Model):
    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        related_name="alerta"
    )

    mensaje = models.CharField(
        max_length=255
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.mensaje