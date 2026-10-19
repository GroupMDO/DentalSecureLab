from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient
from .forms import PatientForm


@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(
        request,
        'patients/patient_list.html',
        {'patients': patients}
    )


@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()

    return render(
        request,
        'patients/patient_form.html',
        {
            'form': form,
            'title': 'Nuevo paciente'
        }
    )


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    return render(
        request,
        'patients/patient_detail.html',
        {'patient': patient}
    )


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)

        if form.is_valid():
            form.save()
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)

    return render(
        request,
        'patients/patient_form.html',
        {
            'form': form,
            'title': 'Editar paciente'
        }
    )


@login_required
def patient_delete(request, pk):
    es_admin = request.user.is_superuser or request.user.groups.filter(name="Administrador").exists()
    if not es_admin:
        return render(
            request,
            "403.html",
            {"exception": "Solo los usuarios con rol Administrador tienen autorización para eliminar pacientes."},
            status=403,
        )

    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')

    return render(
        request,
        'patients/patient_confirm_delete.html',
        {'patient': patient}
    )
