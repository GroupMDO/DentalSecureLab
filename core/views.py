from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from patients.models import Patient
from agenda.models import Appointment
from records.models import MedicalRecord
from payments.models import Payment


@login_required(login_url="/usuarios/login/")
def dashboard(request):

    today = timezone.localdate()

    total_patients = Patient.objects.count()

    today_appointments = Appointment.objects.filter(
        date=today
    ).count()

    total_records = MedicalRecord.objects.count()

    total_payments = sum(
        payment.amount
        for payment in Payment.objects.all()
    )

    context = {
        'total_patients': total_patients,
        'today_appointments': today_appointments,
        'total_records': total_records,
        'total_payments': total_payments,
    }

    return render(
        request,
        'dashboard.html',
        context
    )