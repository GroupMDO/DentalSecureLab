from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import MedicalRecord
from .forms import MedicalRecordForm


def obtener_rol_usuario(user):
    if user.is_superuser:
        return "Administrador"
    grupos = list(user.groups.values_list('name', flat=True))
    if "Soporte" in grupos:
        return "Soporte TI"
    if "Recepción" in grupos or "Recepcion" in grupos:
        return "Recepción"
    if "Doctor" in grupos:
        return "Doctor"
    if "Operador" in grupos:
        return "Operador"
    if "Administrador" in grupos:
        return "Administrador"
    return "Usuario Estándar" if not grupos else ", ".join(grupos)


def tiene_acceso_expedientes(user):
    # 1. Bloqueo explícito a Soporte y Recepción
    if user.groups.filter(name__in=["Soporte", "Recepción", "Recepcion"]).exists():
        return False

    # 2. Principio Default Deny: Solo se permite si es superusuario o tiene rol autorizado
    es_autorizado = (
        user.is_superuser or 
        user.groups.filter(name__in=["Administrador", "Operador", "Doctor"]).exists()
    )
    return es_autorizado


def verificar_acceso_expedientes(request_or_user):
    """
    Control de acceso a expedientes clínicos (ASVS Nivel 2).
    Si se proporciona un HttpRequest y el usuario no está autorizado, retorna una respuesta
    HTTP 403 con la plantilla personalizada 'records/access_denied.html'.
    Si se pasa un objeto User y no está autorizado, lanza PermissionDenied.
    """
    user = getattr(request_or_user, 'user', request_or_user)
    if not tiene_acceso_expedientes(user):
        if hasattr(request_or_user, 'user'):
            rol = obtener_rol_usuario(user)
            es_soporte = user.groups.filter(name="Soporte").exists()
            es_recepcion = user.groups.filter(name__in=["Recepción", "Recepcion"]).exists()
            contexto = {
                "rol_usuario": rol,
                "es_soporte": es_soporte,
                "es_recepcion": es_recepcion,
            }
            return render(request_or_user, "records/access_denied.html", contexto, status=403)
        raise PermissionDenied("Acceso denegado a expedientes clínicos.")
    return None


@login_required
def record_list(request):
    denegado = verificar_acceso_expedientes(request)
    if denegado:
        return denegado
    records = MedicalRecord.objects.select_related('patient').all()
    return render(
        request,
        'records/record_list.html',
        {'records': records}
    )


@login_required
def record_create(request):
    denegado = verificar_acceso_expedientes(request)
    if denegado:
        return denegado

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)

        if form.is_valid():
            record = form.save()
            return redirect('record_detail', pk=record.pk)
    else:
        form = MedicalRecordForm()

    return render(
        request,
        'records/record_form.html',
        {
            'form': form,
            'title': 'Nuevo expediente'
        }
    )


@login_required
def record_detail(request, pk):
    denegado = verificar_acceso_expedientes(request)
    if denegado:
        return denegado

    record = get_object_or_404(
        MedicalRecord,
        pk=pk
    )

    return render(
        request,
        'records/record_detail.html',
        {'record': record}
    )


@login_required
def record_update(request, pk):
    denegado = verificar_acceso_expedientes(request)
    if denegado:
        return denegado

    record = get_object_or_404(
        MedicalRecord,
        pk=pk
    )

    if request.method == 'POST':
        form = MedicalRecordForm(
            request.POST,
            instance=record
        )

        if form.is_valid():
            form.save()
            return redirect(
                'record_detail',
                pk=record.pk
            )
    else:
        form = MedicalRecordForm(
            instance=record
        )

    return render(
        request,
        'records/record_form.html',
        {
            'form': form,
            'title': 'Editar expediente'
        }
    )