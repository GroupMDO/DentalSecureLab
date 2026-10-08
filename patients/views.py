from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Patient
from .forms import PatientForm


def es_doctor(user):
    return user.is_authenticated and user.groups.filter(name='Doctor').exists()


def patient_list(request):
    if not request.user.is_authenticated:
        raise PermissionDenied

    if es_doctor(request.user):
        patients = Patient.objects.filter(doctor_asignado=request.user)
    else:
        patients = Patient.objects.all()

    return render(
        request,
        'patients/patient_list.html',
        {'patients': patients}
    )


def patient_create(request):
    if not request.user.is_authenticated:
        raise PermissionDenied

    if request.method == 'POST':
        form = PatientForm(request.POST)

        if form.is_valid():
            patient = form.save(commit=False)

            if es_doctor(request.user):
                patient.doctor_asignado = request.user

            patient.save()
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


def patient_detail(request, pk):
    if not request.user.is_authenticated:
        raise PermissionDenied

    if es_doctor(request.user):
        patient = get_object_or_404(
            Patient,
            pk=pk,
            doctor_asignado=request.user
        )
    else:
        patient = get_object_or_404(Patient, pk=pk)

    return render(
        request,
        'patients/patient_detail.html',
        {'patient': patient}
    )


def patient_update(request, pk):
    if not request.user.is_authenticated:
        raise PermissionDenied

    if es_doctor(request.user):
        patient = get_object_or_404(
            Patient,
            pk=pk,
            doctor_asignado=request.user
        )
    else:
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


def patient_delete(request, pk):
    if not request.user.is_authenticated:
        raise PermissionDenied

    if es_doctor(request.user):
        patient = get_object_or_404(
            Patient,
            pk=pk,
            doctor_asignado=request.user
        )
    else:
        patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')

    return render(
        request,
        'patients/patient_confirm_delete.html',
        {'patient': patient}
    )