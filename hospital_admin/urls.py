from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='hospital_admin_dashboard'),

    # Department Management
    path('departments/', views.departments, name='ha_departments'),
    path('departments/add/', views.department_create, name='ha_department_create'),
    path('departments/<int:pk>/edit/', views.department_update, name='ha_department_update'),
    path('departments/<int:pk>/deactivate/', views.department_deactivate, name='ha_department_deactivate'),
    path('departments/<int:pk>/activate/', views.department_activate, name='ha_department_activate'),

    # Doctor Management
    path('doctors/', views.doctors, name='ha_doctors'),
    path('doctors/add/', views.doctor_create, name='ha_doctor_create'),
    path('doctors/<int:pk>/edit/', views.doctor_update, name='ha_doctor_update'),
    path('doctors/<int:pk>/deactivate/', views.doctor_deactivate, name='ha_doctor_deactivate'),
    path('doctors/<int:pk>/activate/', views.doctor_activate, name='ha_doctor_activate'),

    # Receptionist Management
    path('receptionists/', views.receptionists, name='ha_receptionists'),
    path('receptionists/add/', views.receptionist_create, name='ha_receptionist_create'),
    path('receptionists/<int:pk>/edit/', views.receptionist_update, name='ha_receptionist_update'),
    path('receptionists/<int:pk>/deactivate/', views.receptionist_deactivate, name='ha_receptionist_deactivate'),
    path('receptionists/<int:pk>/activate/', views.receptionist_activate, name='ha_receptionist_activate'),

    # Patient Management
    path('patients/', views.patients, name='ha_patients'),
    path('patients/profile/<int:pk>/', views.patient_profile_detail, name='ha_patient_profile_detail'),
    path('patients/<int:pk>/', views.patient_detail, name='ha_patient_detail'),
    path('patients/<int:pk>/edit/', views.patient_update, name='ha_patient_update'),
    path('patients/<int:pk>/deactivate/', views.patient_deactivate, name='ha_patient_deactivate'),
    path('patients/<int:pk>/activate/', views.patient_activate, name='ha_patient_activate'),

    # Appointment Overview (read-only for Hospital Admin)
    path('appointments/', views.appointments, name='ha_appointments'),
    path('appointments/<int:pk>/', views.appointment_detail, name='ha_appointment_detail'),

    # Medical Records
    path('medical-records/', views.medical_records, name='ha_medical_records'),
    path('medical-records/<int:pk>/', views.medical_record_detail, name='ha_medical_record_detail'),
    # Billing & Invoice Management
    path('invoices/', views.invoices, name='ha_invoices'),
    path('invoices/<int:pk>/', views.invoice_detail, name='ha_invoice_detail'),

    path('website-settings/',views.website_settings,name='ha_website_settings'),
    path('subscription/', views.subscription_info, name='ha_subscription'),
]
