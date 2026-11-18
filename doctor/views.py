
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST

from platform_admin.models import (
    Doctor,
    Appointment,
    MedicalRecord,
    Prescription,
    LabReport,
    HospitalPatient,
)

from .forms import MedicalRecordForm


# --------------------------------------------------
# TEMPORARY TEST DOCTOR
# Replace with session-based doctor lookup later
# --------------------------------------------------

def get_logged_in_doctor(request):
    return get_object_or_404(
        Doctor,
        user__username='doctor.citycare1'
    )


# --------------------------------------------------
# 1. DOCTOR DASHBOARD
# --------------------------------------------------

def dashboard(request):
    doctor = get_logged_in_doctor(request)
    today = timezone.localdate()

    appointments_today = Appointment.objects.filter(
        doctor=doctor,
        hospital=doctor.hospital,
        date=today
    ).select_related(
        'patient__patient__user',
        'department'
    ).order_by('time')

    total_patients = Appointment.objects.filter(
        doctor=doctor,
        hospital=doctor.hospital
    ).values('patient').distinct().count()

    total_records = MedicalRecord.objects.filter(
        doctor=doctor,
        hospital=doctor.hospital
    ).count()

    upcoming_count = Appointment.objects.filter(
        doctor=doctor,
        hospital=doctor.hospital,
        date__gt=today,
        status__in=['Pending', 'Confirmed']
    ).count()

    context = {
        'doctor': doctor,
        'appointments_today': appointments_today,
        'today_count': appointments_today.count(),
        'total_patients': total_patients,
        'total_records': total_records,
        'upcoming_count': upcoming_count,
    }

    return render(request, 'doc_dashboard.html', context)


# --------------------------------------------------
# 2. VIEW APPOINTMENTS
# --------------------------------------------------

def appointments(request):
    doctor = get_logged_in_doctor(request)

    appointment_list = Appointment.objects.filter(
        doctor=doctor,
        hospital=doctor.hospital
    ).select_related(
        'patient__patient__user',
        'department'
    ).order_by('-date', '-time')

    context = {
        'doctor': doctor,
        'appointments': appointment_list,
    }

    return render(request, 'doc_appointments.html', context)


# --------------------------------------------------
# 3. VIEW PATIENTS
# --------------------------------------------------

def patients(request):
    doctor = get_logged_in_doctor(request)

    patient_list = HospitalPatient.objects.filter(
        hospital=doctor.hospital,
        appointments__doctor=doctor
    ).select_related(
        'patient__user'
    ).distinct()

    context = {
        'doctor': doctor,
        'patients': patient_list,
    }

    return render(request, 'doc_patients.html', context)
# --------------------------------------------------
# 4. VIEW MEDICAL RECORDS
# --------------------------------------------------

def medical_records(request):
    doctor = get_logged_in_doctor(request)

    records = MedicalRecord.objects.filter(
        doctor=doctor,
        hospital=doctor.hospital
    ).select_related(
        'patient__patient__user',
        'appointment'
    ).order_by('-created_at')

    context = {
        'doctor': doctor,
        'records': records,
    }

    return render(request, 'doc_medical_records.html', context)


# --------------------------------------------------
# 5. CREATE MEDICAL RECORD
# --------------------------------------------------

def create_medical_record(request):
    doctor = get_logged_in_doctor(request)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)

        if form.is_valid():
            record = form.save(commit=False)

            # Automatically assign doctor and hospital
            record.doctor = doctor
            record.hospital = doctor.hospital

            # Validate patient
            if not HospitalPatient.objects.filter(
                pk=record.patient.pk,
                hospital=doctor.hospital
            ).exists():
                messages.error(request, 'Invalid patient selected.')
                return redirect('doctor_create_medical_record')

            # Validate appointment
            if not Appointment.objects.filter(
                pk=record.appointment.pk,
                doctor=doctor,
                hospital=doctor.hospital,
                patient=record.patient
            ).exists():
                messages.error(request, 'Invalid appointment selected.')
                return redirect('doctor_create_medical_record')

            # Prevent duplicate medical records
            if MedicalRecord.objects.filter(
                appointment=record.appointment
            ).exists():
                messages.error(
                    request,
                    'A medical record already exists for this appointment.'
                )
                return redirect('doctor_create_medical_record')

            record.save()

            messages.success(
                request,
                'Medical record created successfully.'
            )

            return redirect('doctor_medical_records')

    else:
        form = MedicalRecordForm()

    # Restrict dropdowns to this doctor's hospital
    form.fields['patient'].queryset = HospitalPatient.objects.filter(
        hospital=doctor.hospital
    )

    form.fields['appointment'].queryset = Appointment.objects.filter(
        doctor=doctor,
        hospital=doctor.hospital
    )

    context = {
        'form': form,
        'doctor': doctor,
        'title': 'Create Medical Record',
    }

    return render(request, 'doc_medical_record_form.html', context)


# --------------------------------------------------
# 6. EDIT MEDICAL RECORD
# --------------------------------------------------

def edit_medical_record(request, record_id):
    doctor = get_logged_in_doctor(request)

    record = get_object_or_404(
        MedicalRecord,
        id=record_id,
        doctor=doctor,
        hospital=doctor.hospital
    )

    if request.method == 'POST':
        form = MedicalRecordForm(
            request.POST,
            instance=record
        )

        if form.is_valid():
            updated_record = form.save(commit=False)

            updated_record.doctor = doctor
            updated_record.hospital = doctor.hospital

            # Validate patient
            if not HospitalPatient.objects.filter(
                pk=updated_record.patient.pk,
                hospital=doctor.hospital
            ).exists():
                messages.error(request, 'Invalid patient selected.')
                return redirect(
                    'doctor_edit_medical_record',
                    record_id=record.id
                )

            # Validate appointment
            if not Appointment.objects.filter(
                pk=updated_record.appointment.pk,
                doctor=doctor,
                hospital=doctor.hospital,
                patient=updated_record.patient
            ).exists():
                messages.error(request, 'Invalid appointment selected.')
                return redirect(
                    'doctor_edit_medical_record',
                    record_id=record.id
                )

            # Prevent assigning an appointment already used by another record
            if MedicalRecord.objects.filter(
                appointment=updated_record.appointment
            ).exclude(pk=record.pk).exists():
                messages.error(
                    request,
                    'A medical record already exists for this appointment.'
                )
                return redirect(
                    'doctor_edit_medical_record',
                    record_id=record.id
                )

            updated_record.save()

            messages.success(
                request,
                'Medical record updated successfully.'
            )

            return redirect('doctor_medical_records')

    else:
        form = MedicalRecordForm(instance=record)

    form.fields['patient'].queryset = HospitalPatient.objects.filter(
        hospital=doctor.hospital
    )

    form.fields['appointment'].queryset = Appointment.objects.filter(
        doctor=doctor,
        hospital=doctor.hospital
    )

    context = {
        'form': form,
        'doctor': doctor,
        'title': 'Edit Medical Record',
    }

    return render(request, 'doc_medical_record_form.html', context)


# --------------------------------------------------
# 7. DELETE MEDICAL RECORD
# --------------------------------------------------

@require_POST
def delete_medical_record(request, record_id):
    doctor = get_logged_in_doctor(request)

    record = get_object_or_404(
        MedicalRecord,
        id=record_id,
        doctor=doctor,
        hospital=doctor.hospital
    )

    record.delete()

    messages.success(
        request,
        'Medical record deleted successfully.'
    )

    return redirect('doctor_medical_records')


# --------------------------------------------------
# 8. VIEW PRESCRIPTIONS
# --------------------------------------------------

def prescriptions(request):
    doctor = get_logged_in_doctor(request)

    prescription_list = Prescription.objects.filter(
        doctor=doctor,
        hospital=doctor.hospital
    ).select_related(
        'patient__patient__user',
        'appointment'
    ).prefetch_related(
        'medicines'
    ).order_by('-created_at')

    context = {
        'doctor': doctor,
        'prescriptions': prescription_list,
    }

    return render(request, 'doc_prescriptions.html', context)


# --------------------------------------------------
# 9. VIEW LAB REPORTS
# --------------------------------------------------

def lab_reports(request):
    doctor = get_logged_in_doctor(request)

    reports = LabReport.objects.filter(
        doctor=doctor,
        hospital=doctor.hospital
    ).select_related(
        'patient__patient__user',
        'appointment'
    ).order_by('-test_date')

    context = {
        'doctor': doctor,
        'lab_reports': reports,
    }

    return render(request, 'doc_lab_reports.html', context)
