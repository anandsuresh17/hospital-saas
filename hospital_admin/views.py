
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from django.db.models import Q, Sum
from django.utils.dateparse import parse_date

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
from platform_admin.forms import HospitalWebsiteForm

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
# APPOINTMENT OVERVIEW - READ ONLY
# ==========================================

def appointments(request):

    hospital = get_test_hospital()
    today = timezone.localdate()

    # Base queryset: only appointments belonging to this hospital.
    appointment_list = Appointment.objects.filter(
        hospital=hospital
    ).select_related(
        'patient__patient__user',
        'doctor__user',
        'department'
    ).order_by('-date', '-time')

    # Dashboard statistics are independent of search and filters.
    hospital_appointments = Appointment.objects.filter(
        hospital=hospital
    )

    total_appointments = hospital_appointments.count()
    today_appointments = hospital_appointments.filter(date=today).count()
    pending_appointments = hospital_appointments.filter(status='Pending').count()
    confirmed_appointments = hospital_appointments.filter(status='Confirmed').count()
    completed_appointments = hospital_appointments.filter(status='Completed').count()
    cancelled_appointments = hospital_appointments.filter(status='Cancelled').count()

    # Search by patient name, username, patient ID, doctor or department.
    search_query = request.GET.get('q', '').strip()

    if search_query:
        appointment_list = appointment_list.filter(
            Q(patient__patient__user__first_name__icontains=search_query) |
            Q(patient__patient__user__last_name__icontains=search_query) |
            Q(patient__patient__user__username__icontains=search_query) |
            Q(patient__patient_id_code__icontains=search_query) |
            Q(doctor__user__username__icontains=search_query) |
            Q(doctor__user__first_name__icontains=search_query) |
            Q(doctor__user__last_name__icontains=search_query) |
            Q(department__name__icontains=search_query)
        )

    # Doctor filter.
    doctor_id = request.GET.get('doctor', '').strip()

    if doctor_id.isdigit():
        appointment_list = appointment_list.filter(doctor_id=int(doctor_id))
    else:
        doctor_id = ''

    # Department filter.
    department_id = request.GET.get('department', '').strip()

    if department_id.isdigit():
        appointment_list = appointment_list.filter(department_id=int(department_id))
    else:
        department_id = ''

    # Date filter. Invalid date input is ignored.
    appointment_date = request.GET.get('date', '').strip()
    parsed_date = parse_date(appointment_date) if appointment_date else None

    if parsed_date:
        appointment_list = appointment_list.filter(date=parsed_date)
    else:
        appointment_date = ''

    # Status filter.
    selected_status = request.GET.get('status', '').strip()
    valid_statuses = [choice[0] for choice in Appointment.STATUS_CHOICES]

    if selected_status in valid_statuses:
        appointment_list = appointment_list.filter(status=selected_status)
    else:
        selected_status = ''

    # Dropdown options are restricted to this hospital.
    doctor_list = Doctor.objects.filter(
        hospital=hospital
    ).select_related('user').order_by('user__username')

    department_list = Department.objects.filter(
        hospital=hospital
    ).order_by('name')

    context = {
        'hospital': hospital,
        'appointments': appointment_list,

        'total_appointments': total_appointments,
        'today_appointments': today_appointments,
        'pending_appointments': pending_appointments,
        'confirmed_appointments': confirmed_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,

        'doctors': doctor_list,
        'departments': department_list,
        'appointment_status_choices': Appointment.STATUS_CHOICES,

        'search_query': search_query,
        'selected_doctor': doctor_id,
        'selected_department': department_id,
        'selected_date': appointment_date,
        'selected_status': selected_status,
    }

    return render(
        request,
        'ha_appointments.html',
        context
    )


# ==========================================
# APPOINTMENT DETAILS - READ ONLY
# ==========================================

def appointment_detail(request, pk):

    hospital = get_test_hospital()

    appointment = get_object_or_404(
        Appointment.objects.select_related(
            'hospital',
            'patient__patient__user',
            'doctor__user',
            'department'
        ),
        pk=pk,
        hospital=hospital
    )

    context = {
        'appointment': appointment,
    }

    return render(
        request,
        'ha_appointment_detail.html',
        context
    )

# ==========================================
# BILLING & INVOICE OVERVIEW
# ==========================================

def invoices(request):
    hospital = get_test_hospital()

    # Get invoices belonging to the selected hospital
    invoice_queryset = Invoice.objects.filter(
        hospital=hospital
    ).select_related(
        'patient__patient__user',
        'appointment',
        'appointment__doctor__user',
        'appointment__department',
    ).order_by('-created_at')

    # Dashboard statistics
    total_invoices = invoice_queryset.count()

    paid_invoices = invoice_queryset.filter(
        payment_status="Paid"
    ).count()

    pending_invoices = invoice_queryset.filter(
        payment_status="Pending"
    ).count()

    cancelled_invoices = invoice_queryset.filter(
        payment_status="Cancelled"
    ).count()

    # Total collected from paid invoices
    total_revenue = invoice_queryset.filter(
        payment_status="Paid"
    ).aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    # Search
    search_query = request.GET.get('q', '').strip()

    if search_query:
        search_filter = (
            Q(patient__patient__user__first_name__icontains=search_query) |
            Q(patient__patient__user__last_name__icontains=search_query) |
            Q(patient__patient__user__username__icontains=search_query) |
            Q(patient__patient_id_code__icontains=search_query)
        )

        if search_query.isdigit():
            search_filter |= Q(id=int(search_query))

        invoice_queryset = invoice_queryset.filter(search_filter)

    # Payment status filter
    selected_status = request.GET.get('status', '')

    valid_statuses = [
        value for value, label in Invoice.PAYMENT_STATUS_CHOICES
    ]

    if selected_status in valid_statuses:
        invoice_queryset = invoice_queryset.filter(
            payment_status=selected_status
        )
    else:
        selected_status = ''

    # Date filter
    selected_date = request.GET.get('date', '')

    if selected_date:
        parsed_date = parse_date(selected_date)

        if parsed_date:
            invoice_queryset = invoice_queryset.filter(
                created_at__date=parsed_date
            )
        else:
            selected_date = ''

    context = {
        'hospital': hospital,
        'invoices': invoice_queryset,

        # Statistics
        'total_invoices': total_invoices,
        'paid_invoices': paid_invoices,
        'pending_invoices': pending_invoices,
        'cancelled_invoices': cancelled_invoices,
        'total_revenue': total_revenue,

        # Filters
        'search_query': search_query,
        'selected_status': selected_status,
        'selected_date': selected_date,
        'payment_status_choices': Invoice.PAYMENT_STATUS_CHOICES,
    }

    return render(request, 'ha_invoices.html', context)


# ==========================================
# INVOICE DETAIL
# ==========================================

def invoice_detail(request, pk):
    hospital = get_test_hospital()

    invoice = get_object_or_404(
        Invoice.objects.select_related(
            'hospital',
            'patient__patient__user',
            'appointment',
            'appointment__doctor__user',
            'appointment__department',
        ),
        pk=pk,
        hospital=hospital,
    )

    context = {
        'hospital': hospital,
        'invoice': invoice,
    }

    return render(
        request,
        'ha_invoice_detail.html',
        context
    )

# ==========================================
# HOSPITAL WEBSITE MANAGEMENT
# ==========================================

def website_settings(request):
    hospital = get_test_hospital()

    if request.method == "POST":
        form = HospitalWebsiteForm(
            request.POST,
            request.FILES,
            instance=hospital
        )

        if form.is_valid():
            form.save()
            return redirect('ha_website_settings')

    else:
        form = HospitalWebsiteForm(instance=hospital)

    context = {
        'hospital': hospital,
        'form': form,
    }

    return render(
        request,
        'ha_website_settings.html',
        context
    )
def subscription_info(request):
    hospital = get_test_hospital()

    context = {
        'hospital': hospital,
        'plan': hospital.subscription_plan,
    }

    return render(request, 'ha_subscription.html', context)