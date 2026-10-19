from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Payment
from .forms import PaymentForm


@login_required
def payment_list(request):

    payments = Payment.objects.select_related('patient').all()

    return render(
        request,
        'payments/payment_list.html',
        {'payments': payments}
    )


@login_required
def payment_create(request):

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