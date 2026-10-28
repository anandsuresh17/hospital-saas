from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='reception_dashboard'),

    path('patients/', views.patients, name='reception_patients'),
    path('patients/add/', views.patient_create, name='reception_patient_create'),

    path('appointments/', views.appointments, name='reception_appointments'),
    path('appointments/add/', views.appointment_create, name='reception_appointment_create'),

    path('billing/', views.billing, name='reception_billing'),
    path('billing/<int:pk>/', views.invoice_detail, name='reception_invoice_detail'),
]