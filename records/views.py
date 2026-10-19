from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import MedicalRecord
from .forms import MedicalRecordForm


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
def record_list(request):
    verificar_acceso_expedientes(request.user)
    records = MedicalRecord.objects.select_related('patient').all()
    return render(
        request,
        'records/record_list.html',
        {'records': records}
    )


@login_required
def record_create(request):
    verificar_acceso_expedientes(request.user)

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
    verificar_acceso_expedientes(request.user)

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
    verificar_acceso_expedientes(request.user)

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