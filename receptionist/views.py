from django.shortcuts import render


def dashboard(request):
    return render(request, 'rec_dashboard.html')


def patients(request):
    return render(request, 'rec_patients.html')


def patient_create(request):
    return render(request, 'rec_patient_form.html')


def appointments(request):
    return render(request, 'rec_appointments.html')


def appointment_create(request):
    return render(request, 'rec_appointment_form.html')


def billing(request):
    return render(request, 'rec_billing.html')


def invoice_detail(request, pk):
    return render(request, 'rec_invoice_detail.html', {
        'record_id': pk,
    })