
from django.shortcuts import render


def dashboard(request):
    return render(request, 'pat_dashboard.html')


def profile(request):
    return render(request, 'pat_profile.html')


def appointments(request):
    return render(request, 'pat_appointments.html')


def appointment_form(request):
    return render(request, 'pat_appointment_form.html')


def medical_records(request):
    return render(request, 'pat_medical_records.html')


def prescriptions(request):
    return render(request, 'pat_prescriptions.html')


def lab_reports(request):
    return render(request, 'pat_lab_reports.html')


def invoices(request):
    return render(request, 'pat_invoices.html')
