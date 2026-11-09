
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='hospital_admin_dashboard'),
    path('departments/', views.departments, name='ha_departments'),
    path('doctors/', views.doctors, name='ha_doctors'),
    path('doctors/add/', views.doctor_create, name='ha_doctor_create'),
    path('doctors/<int:pk>/edit/', views.doctor_update, name='ha_doctor_update'),
    path('doctors/<int:pk>/deactivate/', views.doctor_deactivate, name='ha_doctor_deactivate'),
    path('doctors/<int:pk>/activate/', views.doctor_activate, name='ha_doctor_activate'),

    path('receptionists/', views.receptionists, name='ha_receptionists'),
    path('patients/', views.patients, name='ha_patients'),
    path('appointments/', views.appointments, name='ha_appointments'),
    path('departments/add/', views.department_create, name='ha_department_create'),
    path( 'departments/<int:pk>/edit/', views.department_update, name='ha_department_update'),
    path('departments/<int:pk>/deactivate/',views.department_deactivate,name='ha_department_deactivate'),
    path('departments/<int:pk>/activate/',views.department_activate,name='ha_department_activate'),
]
