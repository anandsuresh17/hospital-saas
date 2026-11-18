
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='doctor_dashboard'),

    # Appointments
    path('appointments/', views.appointments, name='doctor_appointments'),

    # Patients
    path('patients/', views.patients, name='doctor_patients'),

    # Medical Records
    path('medical-records/', views.medical_records, name='doctor_medical_records'),

    path(
        'medical-records/create/',
        views.create_medical_record,
        name='doctor_create_medical_record'
    ),

    path(
        'medical-records/<int:record_id>/edit/',
        views.edit_medical_record,
        name='doctor_edit_medical_record'
    ),

    path(
        'medical-records/<int:record_id>/delete/',
        views.delete_medical_record,
        name='doctor_delete_medical_record'
    ),

    # Prescriptions
    path('prescriptions/', views.prescriptions, name='doctor_prescriptions'),

    # Lab Reports
    path('lab-reports/', views.lab_reports, name='doctor_lab_reports'),
]
