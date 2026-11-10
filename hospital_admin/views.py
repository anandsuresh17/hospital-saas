
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q

from platform_admin.models import (
    Hospital,
    Department,
    Doctor,
    Receptionist,
    Patient,
    HospitalPatient,
    Appointment,
    MedicalRecord,
    Prescription,
    LabReport,
    Invoice,
)

from .forms import (
    DepartmentForm,
    DoctorCreateForm,
    DoctorUpdateForm,
    ReceptionistCreateForm,
    ReceptionistUpdateForm,
    PatientUpdateForm,
)


# ==========================================
# TEMPORARY HOSPITAL SELECTION
# ==========================================

def get_test_hospital():
    return Hospital.objects.get(
        email="citycare@example.com"
    )


# ==========================================
# DASHBOARD
# ==========================================

def dashboard(request):

    hospital = get_test_hospital()

    context = {
        'hospital': hospital,

        'total_departments': Department.objects.filter(
            hospital=hospital
        ).count(),

        'total_doctors': Doctor.objects.filter(
            hospital=hospital
        ).count(),

        'total_receptionists': Receptionist.objects.filter(
            hospital=hospital
        ).count(),

        'total_patients': HospitalPatient.objects.filter(
            hospital=hospital
        ).count(),

        'total_appointments': Appointment.objects.filter(
            hospital=hospital
        ).count(),
    }

    return render(request, 'ha_dashboard.html', context)


# ==========================================
# DEPARTMENT MANAGEMENT
# ==========================================

def departments(request):

    hospital = get_test_hospital()

    department_list = Department.objects.filter(
        hospital=hospital
    ).order_by('id')

    return render(
        request,
        'ha_departments.html',
        {'departments': department_list}
    )


def department_create(request):

    hospital = get_test_hospital()

    if request.method == 'POST':

        form = DepartmentForm(request.POST)

        if form.is_valid():

            department = form.save(commit=False)
            department.hospital = hospital
            department.save()

            return redirect('ha_departments')

    else:
        form = DepartmentForm()

    return render(
        request,
        'ha_department_form.html',
        {'form': form}
    )


def department_update(request, pk):

    hospital = get_test_hospital()

    department = get_object_or_404(
        Department,
        pk=pk,
        hospital=hospital
    )

    if request.method == 'POST':

        form = DepartmentForm(
            request.POST,
            instance=department
        )

        if form.is_valid():
            form.save()
            return redirect('ha_departments')

    else:
        form = DepartmentForm(instance=department)

    return render(
        request,
        'ha_department_form.html',
        {
            'form': form,
            'department': department
        }
    )


def department_deactivate(request, pk):

    hospital = get_test_hospital()

    department = get_object_or_404(
        Department,
        pk=pk,
        hospital=hospital
    )

    if request.method == 'POST':

        department.is_active = False
        department.save(update_fields=['is_active'])

        return redirect('ha_departments')

    return render(
        request,
        'ha_department_confirm_deactivate.html',
        {'department': department}
    )


def department_activate(request, pk):

    hospital = get_test_hospital()

    department = get_object_or_404(
        Department,
        pk=pk,
        hospital=hospital
    )

    if request.method == 'POST':

        department.is_active = True
        department.save(update_fields=['is_active'])

        return redirect('ha_departments')

    return render(
        request,
        'ha_department_confirm_activate.html',
        {'department': department}
    )


# ==========================================
# DOCTOR MANAGEMENT
# ==========================================

def doctors(request):

    hospital = get_test_hospital()

    doctor_list = Doctor.objects.filter(
        hospital=hospital
    ).select_related(
        'user',
        'department'
    ).order_by('id')

    return render(
        request,
        'ha_doctors.html',
        {'doctors': doctor_list}
    )


def doctor_create(request):

    hospital = get_test_hospital()

    if request.method == 'POST':

        form = DoctorCreateForm(
            request.POST,
            hospital=hospital
        )

        if form.is_valid():

            data = form.cleaned_data

            with transaction.atomic():

                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password']
                )

                Doctor.objects.create(
                    user=user,
                    hospital=hospital,
                    department=data['department'],
                    qualification=data['qualification'],
                    specialization=data['specialization'],
                    experience_years=data['experience_years'],
                    consultation_fee=data['consultation_fee'],
                    op_commission_percentage=data['op_commission_percentage'],
                    contact_number=data['contact_number'],
                    available_days=data['available_days'],
                    available_time_start=data['available_time_start'],
                    available_time_end=data['available_time_end'],
                )

            return redirect('ha_doctors')

    else:
        form = DoctorCreateForm(hospital=hospital)

    return render(
        request,
        'ha_doctor_form.html',
        {'form': form}
    )


def doctor_update(request, pk):

    hospital = get_test_hospital()

    doctor = get_object_or_404(
        Doctor,
        pk=pk,
        hospital=hospital
    )

    if request.method == 'POST':

        form = DoctorUpdateForm(
            request.POST,
            instance=doctor,
            hospital=hospital
        )

        if form.is_valid():
            form.save()
            return redirect('ha_doctors')

    else:
        form = DoctorUpdateForm(
            instance=doctor,
            hospital=hospital
        )

    return render(
        request,
        'ha_doctor_form.html',
        {
            'form': form,
            'doctor': doctor
        }
    )


def doctor_deactivate(request, pk):

    hospital = get_test_hospital()

    doctor = get_object_or_404(
        Doctor,
        pk=pk,
        hospital=hospital
    )

    if request.method == 'POST':

        doctor.user.is_active = False
        doctor.user.save(update_fields=['is_active'])

        return redirect('ha_doctors')

    return render(
        request,
        'ha_doctor_confirm_deactivate.html',
        {'doctor': doctor}
    )


def doctor_activate(request, pk):

    hospital = get_test_hospital()

    doctor = get_object_or_404(
        Doctor,
        pk=pk,
        hospital=hospital
    )

    if request.method == 'POST':

        doctor.user.is_active = True
        doctor.user.save(update_fields=['is_active'])

        return redirect('ha_doctors')

    return render(
        request,
        'ha_doctor_confirm_activate.html',
        {'doctor': doctor}
    )


# ==========================================
# RECEPTIONIST MANAGEMENT
# ==========================================

def receptionists(request):

    hospital = get_test_hospital()

    receptionist_list = Receptionist.objects.filter(
        hospital=hospital
    ).select_related(
        'user'
    ).order_by('id')

    return render(
        request,
        'ha_receptionists.html',
        {'receptionists': receptionist_list}
    )


def receptionist_create(request):

    hospital = get_test_hospital()

    if request.method == 'POST':

        form = ReceptionistCreateForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data

            with transaction.atomic():

                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password']
                )

                receptionist = form.save(commit=False)
                receptionist.user = user
                receptionist.hospital = hospital
                receptionist.save()

            return redirect('ha_receptionists')

    else:
        form = ReceptionistCreateForm()

    return render(
        request,
        'ha_receptionist_form.html',
        {'form': form}
    )


def receptionist_update(request, pk):

    hospital = get_test_hospital()

    receptionist = get_object_or_404(
        Receptionist,
        pk=pk,
        hospital=hospital
    )

    if request.method == 'POST':

        form = ReceptionistUpdateForm(
            request.POST,
            instance=receptionist
        )

        if form.is_valid():

            with transaction.atomic():

                form.save()

                receptionist.user.username = form.cleaned_data['username']
                receptionist.user.email = form.cleaned_data['email']

                receptionist.user.save(
                    update_fields=['username', 'email']
                )

            return redirect('ha_receptionists')

    else:
        form = ReceptionistUpdateForm(instance=receptionist)

    return render(
        request,
        'ha_receptionist_form.html',
        {
            'form': form,
            'receptionist': receptionist
        }
    )


def receptionist_deactivate(request, pk):

    hospital = get_test_hospital()

    receptionist = get_object_or_404(
        Receptionist,
        pk=pk,
        hospital=hospital
    )

    if request.method == 'POST':

        receptionist.user.is_active = False
        receptionist.user.save(update_fields=['is_active'])

        return redirect('ha_receptionists')

    return render(
        request,
        'ha_receptionist_confirm_deactivate.html',
        {'receptionist': receptionist}
    )


def receptionist_activate(request, pk):

    hospital = get_test_hospital()

    receptionist = get_object_or_404(
        Receptionist,
        pk=pk,
        hospital=hospital
    )

    if request.method == 'POST':

        receptionist.user.is_active = True
        receptionist.user.save(update_fields=['is_active'])

        return redirect('ha_receptionists')

    return render(
        request,
        'ha_receptionist_confirm_activate.html',
        {'receptionist': receptionist}
    )


# ==========================================
# PATIENT MANAGEMENT - ALL PATIENT PROFILES
# ==========================================

def patients(request):

    search_query = request.GET.get('q', '').strip()

    # Fetch every unique patient profile in the database.
    # This does not filter by hospital.

    patient_list = Patient.objects.select_related(
        'user'
    ).order_by('-id')

    if search_query:

        patient_list = patient_list.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(contact_number__icontains=search_query)
        )

    return render(
        request,
        'ha_patients.html',
        {
            'patients': patient_list,
            'search_query': search_query
        }
    )


# ==========================================
# GLOBAL PATIENT PROFILE DETAILS
# ==========================================

def patient_profile_detail(request, pk):

    hospital = get_test_hospital()

    # Find the global patient profile
    patient = get_object_or_404(
        Patient.objects.select_related('user'),
        pk=pk
    )

    # Find this patient's registration in the current hospital
    hospital_patient = get_object_or_404(
        HospitalPatient,
        patient=patient,
        hospital=hospital
    )

    # Redirect using the HospitalPatient ID
    return redirect(
        'ha_patient_detail',
        pk=hospital_patient.pk
    )


# ==========================================
# HOSPITAL-SPECIFIC PATIENT DETAILS
# ==========================================
def patient_detail(request, pk):

    hospital = get_test_hospital()

    hospital_patient = get_object_or_404(
        HospitalPatient.objects.select_related(
            'patient__user',
            'hospital'
        ),
        pk=pk,
        hospital=hospital
    )

    patient = hospital_patient.patient

    appointments = Appointment.objects.filter(
        patient=hospital_patient
    ).select_related(
        'doctor__user',
        'department'
    )

    medical_records = MedicalRecord.objects.filter(
        patient=hospital_patient
    ).select_related(
        'doctor__user',
        'appointment'
    )

    prescriptions = Prescription.objects.filter(
        patient=hospital_patient
    ).select_related(
        'doctor__user',
        'appointment'
    ).prefetch_related('medicines')

    lab_reports = LabReport.objects.filter(
        patient=hospital_patient
    ).select_related(
        'doctor__user',
        'appointment'
    )

    invoices = Invoice.objects.filter(
        patient=hospital_patient
    ).select_related(
        'appointment'
    )

    context = {
        'hospital_patient': hospital_patient,
        'patient': patient,
        'appointments': appointments,
        'medical_records': medical_records,
        'prescriptions': prescriptions,
        'lab_reports': lab_reports,
        'invoices': invoices,
    }

    print("========== PATIENT DETAIL DEBUG ==========")
    print("Hospital:", hospital.name)
    print("Hospital Patient ID:", hospital_patient.id)
    print("Patient:", patient.user.username)
    print("Appointments:", appointments.count())
    print("Medical Records:", medical_records.count())
    print("Prescriptions:", prescriptions.count())
    print("Lab Reports:", lab_reports.count())
    print("Invoices:", invoices.count())
    print("==========================================")

    return render(
        request,
        'ha_patient_detail.html',
        context
    )

# ==========================================
# PATIENT UPDATE
# ==========================================

def patient_update(request, pk):

    hospital = get_test_hospital()

    hospital_patient = get_object_or_404(
        HospitalPatient.objects.select_related(
            'patient__user'
        ),
        pk=pk,
        hospital=hospital
    )

    patient = hospital_patient.patient

    if request.method == 'POST':

        form = PatientUpdateForm(
            request.POST,
            instance=patient
        )

        if form.is_valid():

            with transaction.atomic():

                form.save()

                patient.user.first_name = form.cleaned_data['first_name']
                patient.user.last_name = form.cleaned_data['last_name']
                patient.user.email = form.cleaned_data['email']

                patient.user.save(
                    update_fields=[
                        'first_name',
                        'last_name',
                        'email'
                    ]
                )

            return redirect(
                'ha_patient_detail',
                pk=hospital_patient.pk
            )

    else:
        form = PatientUpdateForm(instance=patient)

    return render(
        request,
        'ha_patient_form.html',
        {
            'form': form,
            'hospital_patient': hospital_patient
        }
    )


# ==========================================
# PATIENT DEACTIVATE
# ==========================================

def patient_deactivate(request, pk):

    hospital = get_test_hospital()

    hospital_patient = get_object_or_404(
        HospitalPatient,
        pk=pk,
        hospital=hospital
    )

    if request.method == 'POST':

        hospital_patient.is_active = False
        hospital_patient.save(update_fields=['is_active'])

        return redirect('ha_patients')

    return render(
        request,
        'ha_patient_confirm_deactivate.html',
        {'hospital_patient': hospital_patient}
    )


# ==========================================
# PATIENT ACTIVATE
# ==========================================

def patient_activate(request, pk):

    hospital = get_test_hospital()

    hospital_patient = get_object_or_404(
        HospitalPatient,
        pk=pk,
        hospital=hospital
    )

    if request.method == 'POST':

        hospital_patient.is_active = True
        hospital_patient.save(update_fields=['is_active'])

        return redirect('ha_patients')

    return render(
        request,
        'ha_patient_confirm_activate.html',
        {'hospital_patient': hospital_patient}
    )


# ==========================================
# MEDICAL RECORDS MANAGEMENT
# ==========================================

def medical_records(request):

    hospital = get_test_hospital()

    search_query = request.GET.get('q', '').strip()
    doctor_id = request.GET.get('doctor', '').strip()
    record_date = request.GET.get('date', '').strip()

    records = MedicalRecord.objects.filter(
        hospital=hospital
    ).select_related(
        'patient__patient__user',
        'doctor__user',
        'appointment'
    ).order_by(
        '-appointment__date',
        '-id'
    )

    if search_query:

        records = records.filter(
            Q(patient__patient__user__first_name__icontains=search_query) |
            Q(patient__patient__user__last_name__icontains=search_query) |
            Q(patient__patient__user__username__icontains=search_query) |
            Q(patient__patient_id_code__icontains=search_query) |
            Q(doctor__user__username__icontains=search_query) |
            Q(diagnosis__icontains=search_query)
        )

    if doctor_id:
        records = records.filter(
            doctor_id=doctor_id
        )

    if record_date:
        records = records.filter(
            appointment__date=record_date
        )

    doctor_list = Doctor.objects.filter(
        hospital=hospital
    ).select_related(
        'user'
    ).order_by(
        'user__username'
    )

    context = {
        'records': records,
        'doctors': doctor_list,
        'search_query': search_query,
        'selected_doctor': doctor_id,
        'selected_date': record_date,
    }

    return render(
        request,
        'ha_medical_records.html',
        context
    )


# ==========================================
# MEDICAL RECORD DETAILS
# ==========================================

def medical_record_detail(request, pk):

    hospital = get_test_hospital()

    record = get_object_or_404(
        MedicalRecord.objects.select_related(
            'patient__patient__user',
            'doctor__user',
            'appointment',
            'hospital'
        ),
        pk=pk,
        hospital=hospital
    )

    return render(
        request,
        'ha_medical_record_detail.html',
        {'record': record}
    )


# ==========================================
# APPOINTMENT PLACEHOLDER
# ==========================================

def appointments(request):

    return render(
        request,
        'ha_appointments.html'
    )
