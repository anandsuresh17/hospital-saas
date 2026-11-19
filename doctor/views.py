
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db import transaction

from platform_admin.models import (
    Doctor,
    Appointment,
    MedicalRecord,
    Prescription,
    PrescriptionMedicine,
    LabReport,
    HospitalPatient,
)

from .forms import (
    MedicalRecordForm,
    PrescriptionMedicineFormSet,
    LabReportForm,
)


# --------------------------------------------------
# TEMPORARY TEST DOCTOR
# Replace with session-based lookup later
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

    form = MedicalRecordForm(
        request.POST or None
    )

    form.fields['patient'].queryset = HospitalPatient.objects.filter(
        hospital=doctor.hospital
    )

    form.fields['appointment'].queryset = Appointment.objects.filter(
        doctor=doctor,
        hospital=doctor.hospital
    )

    if request.method == 'POST':

        if form.is_valid():

            record = form.save(commit=False)

            record.doctor = doctor
            record.hospital = doctor.hospital

            valid_appointment = Appointment.objects.filter(
                pk=record.appointment.pk,
                doctor=doctor,
                hospital=doctor.hospital,
                patient=record.patient
            ).exists()

            if not valid_appointment:
                messages.error(request, 'Invalid appointment selected.')

            elif MedicalRecord.objects.filter(
                appointment=record.appointment
            ).exists():

                messages.error(
                    request,
                    'A medical record already exists for this appointment.'
                )

            else:
                record.save()

                messages.success(
                    request,
                    'Medical record created successfully.'
                )

                return redirect('doctor_medical_records')

    return render(
        request,
        'doc_medical_record_form.html',
        {
            'form': form,
            'doctor': doctor,
            'title': 'Create Medical Record',
        }
    )


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

    form = MedicalRecordForm(
        request.POST or None,
        instance=record
    )

    form.fields['patient'].queryset = HospitalPatient.objects.filter(
        hospital=doctor.hospital
    )

    form.fields['appointment'].queryset = Appointment.objects.filter(
        doctor=doctor,
        hospital=doctor.hospital
    )

    if request.method == 'POST':

        if form.is_valid():

            updated_record = form.save(commit=False)

            updated_record.doctor = doctor
            updated_record.hospital = doctor.hospital

            valid_appointment = Appointment.objects.filter(
                pk=updated_record.appointment.pk,
                doctor=doctor,
                hospital=doctor.hospital,
                patient=updated_record.patient
            ).exists()

            duplicate = MedicalRecord.objects.filter(
                appointment=updated_record.appointment
            ).exclude(
                pk=record.pk
            ).exists()

            if not valid_appointment:
                messages.error(request, 'Invalid appointment selected.')

            elif duplicate:
                messages.error(
                    request,
                    'A medical record already exists for this appointment.'
                )

            else:
                updated_record.save()

                messages.success(
                    request,
                    'Medical record updated successfully.'
                )

                return redirect('doctor_medical_records')

    return render(
        request,
        'doc_medical_record_form.html',
        {
            'form': form,
            'doctor': doctor,
            'title': 'Edit Medical Record',
        }
    )


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
# 9. CREATE PRESCRIPTION
# --------------------------------------------------

def create_prescription(request):
    doctor = get_logged_in_doctor(request)

    appointments_list = Appointment.objects.filter(
        doctor=doctor,
        hospital=doctor.hospital
    ).exclude(
        id__in=Prescription.objects.values('appointment_id')
    ).select_related(
        'patient__patient__user'
    ).order_by('-date', '-time')

    if request.method == 'POST':

        appointment_id = request.POST.get('appointment')

        appointment = get_object_or_404(
            appointments_list,
            id=appointment_id
        )

        with transaction.atomic():

            prescription = Prescription.objects.create(
                hospital=doctor.hospital,
                appointment=appointment,
                patient=appointment.patient,
                doctor=doctor
            )

            formset = PrescriptionMedicineFormSet(
                request.POST,
                instance=prescription
            )

            if formset.is_valid():

                active_forms = [
                    form for form in formset.forms
                    if form.has_changed()
                    and not form.cleaned_data.get('DELETE', False)
                ]

                if active_forms:
                    formset.save()

                    messages.success(
                        request,
                        'Prescription created successfully.'
                    )

                    return redirect('doctor_prescriptions')

                prescription.delete()

                messages.error(
                    request,
                    'Please add at least one medicine.'
                )

            else:
                prescription.delete()

    else:
        formset = PrescriptionMedicineFormSet()

    return render(
        request,
        'doc_prescription_form.html',
        {
            'doctor': doctor,
            'appointments': appointments_list,
            'formset': formset,
            'title': 'Create Prescription',
        }
    )


# --------------------------------------------------
# 10. VIEW PRESCRIPTION DETAILS
# --------------------------------------------------

def prescription_detail(request, prescription_id):
    doctor = get_logged_in_doctor(request)

    prescription = get_object_or_404(
        Prescription.objects.select_related(
            'patient__patient__user',
            'appointment'
        ).prefetch_related('medicines'),
        id=prescription_id,
        doctor=doctor,
        hospital=doctor.hospital
    )

    return render(
        request,
        'doc_prescription_detail.html',
        {
            'doctor': doctor,
            'prescription': prescription,
        }
    )


# --------------------------------------------------
# 11. EDIT PRESCRIPTION
# --------------------------------------------------

def edit_prescription(request, prescription_id):
    doctor = get_logged_in_doctor(request)

    prescription = get_object_or_404(
        Prescription,
        id=prescription_id,
        doctor=doctor,
        hospital=doctor.hospital
    )

    formset = PrescriptionMedicineFormSet(
        request.POST or None,
        instance=prescription
    )

    if request.method == 'POST':

        if formset.is_valid():

            remaining_medicines = [
                form for form in formset.forms
                if (
                    form.instance.pk or form.has_changed()
                ) and not form.cleaned_data.get('DELETE', False)
            ]

            if remaining_medicines:

                formset.save()

                messages.success(
                    request,
                    'Prescription updated successfully.'
                )

                return redirect('doctor_prescriptions')

            messages.error(
                request,
                'A prescription must contain at least one medicine.'
            )

    return render(
        request,
        'doc_prescription_form.html',
        {
            'doctor': doctor,
            'prescription': prescription,
            'formset': formset,
            'title': 'Edit Prescription',
        }
    )


# --------------------------------------------------
# 12. DELETE PRESCRIPTION
# --------------------------------------------------

@require_POST
def delete_prescription(request, prescription_id):
    doctor = get_logged_in_doctor(request)

    prescription = get_object_or_404(
        Prescription,
        id=prescription_id,
        doctor=doctor,
        hospital=doctor.hospital
    )

    prescription.delete()

    messages.success(
        request,
        'Prescription deleted successfully.'
    )

    return redirect('doctor_prescriptions')


# --------------------------------------------------
# 13. VIEW LAB REPORTS
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


# --------------------------------------------------
# 14. CREATE LAB REPORT
# --------------------------------------------------

def create_lab_report(request):
    doctor = get_logged_in_doctor(request)

    form = LabReportForm(
        request.POST or None,
        request.FILES or None
    )

    form.fields['patient'].queryset = HospitalPatient.objects.filter(
        hospital=doctor.hospital
    )

    form.fields['appointment'].queryset = Appointment.objects.filter(
        doctor=doctor,
        hospital=doctor.hospital
    )

    if request.method == 'POST':

        if form.is_valid():

            report = form.save(commit=False)

            report.doctor = doctor
            report.hospital = doctor.hospital

            if report.appointment:

                valid_appointment = Appointment.objects.filter(
                    pk=report.appointment.pk,
                    doctor=doctor,
                    hospital=doctor.hospital,
                    patient=report.patient
                ).exists()

                if not valid_appointment:
                    messages.error(
                        request,
                        'Invalid appointment selected.'
                    )

                    return render(
                        request,
                        'doc_lab_report_form.html',
                        {
                            'doctor': doctor,
                            'form': form,
                            'title': 'Create Lab Report',
                        }
                    )

            report.save()

            messages.success(
                request,
                'Lab report created successfully.'
            )

            return redirect('doctor_lab_reports')

    return render(
        request,
        'doc_lab_report_form.html',
        {
            'doctor': doctor,
            'form': form,
            'title': 'Create Lab Report',
        }
    )


# --------------------------------------------------
# 15. EDIT LAB REPORT
# --------------------------------------------------

def edit_lab_report(request, report_id):
    doctor = get_logged_in_doctor(request)

    report = get_object_or_404(
        LabReport,
        id=report_id,
        doctor=doctor,
        hospital=doctor.hospital
    )

    form = LabReportForm(
        request.POST or None,
        request.FILES or None,
        instance=report
    )

    form.fields['patient'].queryset = HospitalPatient.objects.filter(
        hospital=doctor.hospital
    )

    form.fields['appointment'].queryset = Appointment.objects.filter(
        doctor=doctor,
        hospital=doctor.hospital
    )

    if request.method == 'POST':

        if form.is_valid():

            updated_report = form.save(commit=False)

            updated_report.doctor = doctor
            updated_report.hospital = doctor.hospital

            if updated_report.appointment:

                valid_appointment = Appointment.objects.filter(
                    pk=updated_report.appointment.pk,
                    doctor=doctor,
                    hospital=doctor.hospital,
                    patient=updated_report.patient
                ).exists()

                if not valid_appointment:
                    messages.error(
                        request,
                        'Invalid appointment selected.'
                    )

                    return render(
                        request,
                        'doc_lab_report_form.html',
                        {
                            'doctor': doctor,
                            'form': form,
                            'title': 'Edit Lab Report',
                            'report': report,
                        }
                    )

            updated_report.save()

            messages.success(
                request,
                'Lab report updated successfully.'
            )

            return redirect('doctor_lab_reports')

    return render(
        request,
        'doc_lab_report_form.html',
        {
            'doctor': doctor,
            'form': form,
            'title': 'Edit Lab Report',
            'report': report,
        }
    )


# --------------------------------------------------
# 16. DELETE LAB REPORT
# --------------------------------------------------

@require_POST
def delete_lab_report(request, report_id):
    doctor = get_logged_in_doctor(request)

    report = get_object_or_404(
        LabReport,
        id=report_id,
        doctor=doctor,
        hospital=doctor.hospital
    )

    report.delete()

    messages.success(
        request,
        'Lab report deleted successfully.'
    )

    return redirect('doctor_lab_reports')
