
from django.shortcuts import render


def dashboard(request):
    return render(request, 'ha_dashboard.html')


def departments(request):
    return render(request, 'ha_departments.html')


def doctors(request):
    return render(request, 'ha_doctors.html')


def receptionists(request):
    return render(request, 'ha_receptionists.html')


def patients(request):
    return render(request, 'ha_patients.html')


def appointments(request):
    return render(request, 'ha_appointments.html')
