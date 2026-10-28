
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='doctor_dashboard'),
    path('appointments/', views.appointments, name='doctor_appointments'),
    path('patients/', views.patients, name='doctor_patients'),
    path('medical-records/', views.medical_records, name='doctor_medical_records'),
    path('prescriptions/', views.prescriptions, name='doctor_prescriptions'),
    path('lab-reports/', views.lab_reports, name='doctor_lab_reports'),
]
