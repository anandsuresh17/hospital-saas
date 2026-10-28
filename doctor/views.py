
from django.shortcuts import render


def dashboard(request):
    return render(request, 'doc_dashboard.html')


def appointments(request):
    return render(request, 'doc_appointments.html')


def patients(request):
    return render(request, 'doc_patients.html')


def medical_records(request):
    return render(request, 'doc_medical_records.html')


def prescriptions(request):
    return render(request, 'doc_prescriptions.html')


def lab_reports(request):
    return render(request, 'doc_lab_reports.html')
