
from django.urls import path
from . import views


urlpatterns = [

    # =====================================
    # DASHBOARD
    # =====================================

    path(
        '',
        views.dashboard,
        name='hospital_admin_dashboard'
    ),


    # =====================================
    # DEPARTMENT MANAGEMENT
    # =====================================

    path(
        'departments/',
        views.departments,
        name='ha_departments'
    ),

    path(
        'departments/add/',
        views.department_create,
        name='ha_department_create'
    ),

    path(
        'departments/<int:pk>/edit/',
        views.department_update,
        name='ha_department_update'
    ),

    path(
        'departments/<int:pk>/deactivate/',
        views.department_deactivate,
        name='ha_department_deactivate'
    ),

    path(
        'departments/<int:pk>/activate/',
        views.department_activate,
        name='ha_department_activate'
    ),


    # =====================================
    # DOCTOR MANAGEMENT
    # =====================================

    path(
        'doctors/',
        views.doctors,
        name='ha_doctors'
    ),

    path(
        'doctors/add/',
        views.doctor_create,
        name='ha_doctor_create'
    ),

    path(
        'doctors/<int:pk>/edit/',
        views.doctor_update,
        name='ha_doctor_update'
    ),

    path(
        'doctors/<int:pk>/deactivate/',
        views.doctor_deactivate,
        name='ha_doctor_deactivate'
    ),

    path(
        'doctors/<int:pk>/activate/',
        views.doctor_activate,
        name='ha_doctor_activate'
    ),


    # =====================================
    # RECEPTIONIST MANAGEMENT
    # =====================================

    path(
        'receptionists/',
        views.receptionists,
        name='ha_receptionists'
    ),

    path(
        'receptionists/add/',
        views.receptionist_create,
        name='ha_receptionist_create'
    ),

    path(
        'receptionists/<int:pk>/edit/',
        views.receptionist_update,
        name='ha_receptionist_update'
    ),

    path(
        'receptionists/<int:pk>/deactivate/',
        views.receptionist_deactivate,
        name='ha_receptionist_deactivate'
    ),

    path(
        'receptionists/<int:pk>/activate/',
        views.receptionist_activate,
        name='ha_receptionist_activate'
    ),


    # =====================================
    # PATIENT MANAGEMENT
    # =====================================

    # All patient profiles
    path(
        'patients/',
        views.patients,
        name='ha_patients'
    ),

    # Global patient profile details
    path(
        'patients/profile/<int:pk>/',
        views.patient_profile_detail,
        name='ha_patient_profile_detail'
    ),

    # Hospital-specific patient details
    path(
        'patients/<int:pk>/',
        views.patient_detail,
        name='ha_patient_detail'
    ),

    path(
        'patients/<int:pk>/edit/',
        views.patient_update,
        name='ha_patient_update'
    ),

    path(
        'patients/<int:pk>/deactivate/',
        views.patient_deactivate,
        name='ha_patient_deactivate'
    ),

    path(
        'patients/<int:pk>/activate/',
        views.patient_activate,
        name='ha_patient_activate'
    ),


    # =====================================
    # APPOINTMENTS
    # =====================================

    path(
        'appointments/',
        views.appointments,
        name='ha_appointments'
    ),


    # =====================================
    # MEDICAL RECORDS
    # =====================================

    path(
        'medical-records/',
        views.medical_records,
        name='ha_medical_records'
    ),

    path(
        'medical-records/<int:pk>/',
        views.medical_record_detail,
        name='ha_medical_record_detail'
    ),

]
