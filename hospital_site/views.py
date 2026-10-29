
from django.shortcuts import render


def home(request, hospital_slug):
    return render(request, 'hs_home.html', {'hospital_slug': hospital_slug})


def about(request, hospital_slug):
    return render(request, 'hs_about.html', {'hospital_slug': hospital_slug})


def departments(request, hospital_slug):
    return render(request, 'hs_departments.html', {'hospital_slug': hospital_slug})


def doctors(request, hospital_slug):
    return render(request, 'hs_doctors.html', {'hospital_slug': hospital_slug})


def appointment_form(request, hospital_slug):
    return render(request, 'hs_appointment_form.html', {'hospital_slug': hospital_slug})


def contact(request, hospital_slug):
    return render(request, 'hs_contact.html', {'hospital_slug': hospital_slug})
