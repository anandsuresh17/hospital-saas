
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import transaction

from platform_admin.models import (
    Hospital,
    Department,
    Doctor,
    Receptionist,
    HospitalPatient,
    Appointment,
)

from .forms import (
    DepartmentForm,
    DoctorCreateForm,
    DoctorUpdateForm,
)


# TEMPORARY HOSPITAL SELECTION FOR DEVELOPMENT

def get_test_hospital():
    return Hospital.objects.get(email="citycare@example.com")


# DASHBOARD

def dashboard(request):

    hospital = get_test_hospital()

    context = {
        'hospital': hospital,
        'total_departments': Department.objects.filter(hospital=hospital).count(),
        'total_doctors': Doctor.objects.filter(hospital=hospital).count(),
        'total_receptionists': Receptionist.objects.filter(hospital=hospital).count(),
        'total_patients': HospitalPatient.objects.filter(hospital=hospital).count(),
        'total_appointments': Appointment.objects.filter(hospital=hospital).count(),
    }

    return render(request, 'ha_dashboard.html', context)


# DEPARTMENT LIST

def departments(request):

    hospital = get_test_hospital()

    departments = Department.objects.filter(
        hospital=hospital
    ).order_by('id')

    return render(
        request,
        'ha_departments.html',
        {'departments': departments}
    )


# CREATE DEPARTMENT

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


# UPDATE DEPARTMENT

def department_update(request, pk):

    hospital = get_test_hospital()

    department = get_object_or_404(
        Department,
        pk=pk,
        hospital=hospital
    )

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)

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


# DEACTIVATE DEPARTMENT

def department_deactivate(request, pk):

    hospital = get_test_hospital()

    department = get_object_or_404(
        Department,
        pk=pk,
        hospital=hospital
    )

    if request.method == 'POST':
        department.is_active = False
        department.save()
        return redirect('ha_departments')

    return render(
        request,
        'ha_department_confirm_deactivate.html',
        {'department': department}
    )


# ACTIVATE DEPARTMENT

def department_activate(request, pk):

    hospital = get_test_hospital()

    department = get_object_or_404(
        Department,
        pk=pk,
        hospital=hospital
    )

    if request.method == 'POST':
        department.is_active = True
        department.save()
        return redirect('ha_departments')

    return render(
        request,
        'ha_department_confirm_activate.html',
        {'department': department}
    )


# DOCTOR LIST

def doctors(request):

    hospital = get_test_hospital()

    doctors = Doctor.objects.filter(
        hospital=hospital
    ).select_related(
        'user',
        'department'
    ).order_by('id')

    return render(
        request,
        'ha_doctors.html',
        {'doctors': doctors}
    )


# CREATE DOCTOR

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


# UPDATE DOCTOR

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


# DEACTIVATE DOCTOR

def doctor_deactivate(request, pk):

    hospital = get_test_hospital()

    doctor = get_object_or_404(
        Doctor,
        pk=pk,
        hospital=hospital
    )

    if request.method == 'POST':
        doctor.user.is_active = False
        doctor.user.save()

        return redirect('ha_doctors')

    return render(
        request,
        'ha_doctor_confirm_deactivate.html',
        {'doctor': doctor}
    )


# ACTIVATE DOCTOR

def doctor_activate(request, pk):

    hospital = get_test_hospital()

    doctor = get_object_or_404(
        Doctor,
        pk=pk,
        hospital=hospital
    )

    if request.method == 'POST':
        doctor.user.is_active = True
        doctor.user.save()

        return redirect('ha_doctors')

    return render(
        request,
        'ha_doctor_confirm_activate.html',
        {'doctor': doctor}
    )


# OTHER MODULES

def receptionists(request):
    return render(request, 'ha_receptionists.html')


def patients(request):
    return render(request, 'ha_patients.html')


def appointments(request):
    return render(request, 'ha_appointments.html')
