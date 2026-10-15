from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from .models import MedicalRecord
from .forms import MedicalRecordForm


def verificar_acceso_expedientes(request):
    # Bloquear explícitamente a usuarios de los grupos Soporte y Recepción
    if request.user.groups.filter(name__in=["Soporte", "Recepción"]).exists():
        raise PermissionDenied("No tiene permisos para acceder a expedientes clínicos.")


@login_required
def record_list(request):
    verificar_acceso_expedientes(request)
    records = MedicalRecord.objects.select_related('patient').all()
    return render(
        request,
        'records/record_list.html',
        {'records': records}
    )


@login_required
def record_create(request):
    verificar_acceso_expedientes(request)
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
    verificar_acceso_expedientes(request)
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
    verificar_acceso_expedientes(request)
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