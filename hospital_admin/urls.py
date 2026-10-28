
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='hospital_admin_dashboard'),
    path('departments/', views.departments, name='ha_departments'),
    path('doctors/', views.doctors, name='ha_doctors'),
    path('receptionists/', views.receptionists, name='ha_receptionists'),
    path('patients/', views.patients, name='ha_patients'),
    path('appointments/', views.appointments, name='ha_appointments'),
]
