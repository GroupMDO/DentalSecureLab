from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Payment
from .forms import PaymentForm


def verificar_acceso_pagos(request):
    if request.user.groups.filter(name="Soporte").exists() and not request.user.is_superuser:
        return render(
            request,
            "403.html",
            {"exception": "El personal de Soporte TI no tiene permisos para acceder al módulo de pagos."},
            status=403,
        )
    return None


@login_required
def payment_list(request):
    bloqueado = verificar_acceso_pagos(request)
    if bloqueado:
        return bloqueado

    payments = Payment.objects.select_related('patient').all()

    return render(
        request,
        'payments/payment_list.html',
        {'payments': payments}
    )


@login_required
def payment_create(request):
    bloqueado = verificar_acceso_pagos(request)
    if bloqueado:
        return bloqueado

    if request.method == 'POST':
        form = PaymentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('payment_list')

    else:
        form = PaymentForm()

    return render(
        request,
        'payments/payment_form.html',
        {
            'form': form,
            'title': 'Registrar pago'
        }
    )


@login_required
def payment_update(request, pk):
    bloqueado = verificar_acceso_pagos(request)
    if bloqueado:
        return bloqueado

    payment = get_object_or_404(Payment, pk=pk)

    if request.method == 'POST':

        form = PaymentForm(
            request.POST,
            instance=payment
        )

        if form.is_valid():
            form.save()
            return redirect('payment_list')

    else:
        form = PaymentForm(instance=payment)

    return render(
        request,
        'payments/payment_form.html',
        {
            'form': form,
            'title': 'Editar pago'
        }
    )
