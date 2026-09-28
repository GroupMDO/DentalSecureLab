from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import MedicalRecord
from .forms import MedicalRecordForm


def verificar_acceso_clinico(request):
    if not request.user.is_authenticated:
        raise PermissionDenied

    # Temporal: comprobar qué usuario y grupo están entrando
    print("USUARIO:", request.user.username)
    print(
        "GRUPOS:",
        list(request.user.groups.values_list('name', flat=True))
    )

    # Recepción no puede consultar información clínica
    if request.user.groups.filter(name='Recepcion').exists():
        raise PermissionDenied


def record_list(request):
    verificar_acceso_clinico(request)

    records = MedicalRecord.objects.select_related('patient').all()

    return render(
        request,
        'records/record_list.html',
        {'records': records}
    )


def record_create(request):
    verificar_acceso_clinico(request)

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


def record_detail(request, pk):
    verificar_acceso_clinico(request)

    record = get_object_or_404(
        MedicalRecord,
        pk=pk
    )

    return render(
        request,
        'records/record_detail.html',
        {'record': record}
    )


def record_update(request, pk):
    verificar_acceso_clinico(request)

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