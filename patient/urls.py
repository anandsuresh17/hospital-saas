
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='patient_dashboard'),
    path('profile/', views.profile, name='patient_profile'),
    path('appointments/', views.appointments, name='patient_appointments'),
    path('appointments/book/', views.appointment_form, name='patient_appointment_form'),
    path('medical-records/', views.medical_records, name='patient_medical_records'),
    path('prescriptions/', views.prescriptions, name='patient_prescriptions'),
    path('lab-reports/', views.lab_reports, name='patient_lab_reports'),
    path('invoices/', views.invoices, name='patient_invoices'),
]
