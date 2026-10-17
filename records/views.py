from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def verificar_acceso_expedientes(user):
    # 1. Bloqueo explícito a Soporte y Recepción
    if user.groups.filter(name__in=["Soporte", "Recepción", "Recepcion"]).exists():
        raise PermissionDenied("No tiene permisos para acceder a expedientes clínicos.")

    # 2. Principio Default Deny: Solo se permite si es superusuario o tiene rol autorizado
    es_autorizado = (
        user.is_superuser or 
        user.groups.filter(name__in=["Administrador", "Operador", "Doctor"]).exists()
    )

    if not es_autorizado:
        raise PermissionDenied("Acceso denegado a expedientes clínicos.")


@login_required
def lista_expedientes(request):
    verificar_acceso_expedientes(request.user)
    return HttpResponse("Lista de Expedientes Clínicos")