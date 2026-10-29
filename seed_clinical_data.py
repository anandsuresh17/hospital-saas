
import os
import django
from datetime import date, time, timedelta
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.db import transaction
from django.contrib.auth.models import User
from platform_admin.models import (
    Hospital, Doctor, Patient, HospitalPatient,
    Department, Appointment, MedicalRecord,
    Prescription, PrescriptionMedicine, LabReport, Invoice
)


@transaction.atomic
def seed_clinical_data():
    # Fetch existing hospitals
    citycare = Hospital.objects.get(name="City Care Hospital")
    metro = Hospital.objects.get(name="Metro Medical Centre")
    greenlife = Hospital.objects.get(name="Green Life Hospital")

    # Fetch existing doctors
    city_doctor = Doctor.objects.get(user__username="doctor.citycare1")
    metro_doctor = Doctor.objects.get(user__username="doctor.metro1")
    green_doctor = Doctor.objects.get(user__username="doctor.greenlife1")

    # Fetch existing hospital registrations
    arun_city = HospitalPatient.objects.get(
        hospital=citycare,
        patient__user__username="patient.arun"
    )
    arun_metro = HospitalPatient.objects.get(
        hospital=metro,
        patient__user__username="patient.arun"
    )
    anu_green = HospitalPatient.objects.get(
        hospital=greenlife,
        patient__user__username="patient.anu"
    )

    # Fetch departments
    city_cardio = Department.objects.get(hospital=citycare, name="Cardiology")
    metro_neuro = Department.objects.get(hospital=metro, name="Neurology")
    green_derma = Department.objects.get(hospital=greenlife, name="Dermatology")

    today = date.today()

    with transaction.atomic():
        # 1. Appointments
        appointment1, _ = Appointment.objects.get_or_create(
            hospital=citycare,
            patient=arun_city,
            doctor=city_doctor,
            department=city_cardio,
            date=today,
            time=time(10, 0),
            defaults={
                "reason": "Routine heart check-up",
                "status": "Confirmed",
            },
        )

        appointment2, _ = Appointment.objects.get_or_create(
            hospital=metro,
            patient=arun_metro,
            doctor=metro_doctor,
            department=metro_neuro,
            date=today + timedelta(days=1),
            time=time(11, 0),
            defaults={
                "reason": "Recurring headache",
                "status": "Confirmed",
            },
        )

        appointment3, _ = Appointment.objects.get_or_create(
            hospital=greenlife,
            patient=anu_green,
            doctor=green_doctor,
            department=green_derma,
            date=today,
            time=time(14, 0),
            defaults={
                "reason": "Skin consultation",
                "status": "Completed",
            },
        )

        # 2. Medical records
        MedicalRecord.objects.get_or_create(
            appointment=appointment1,
            defaults={
                "hospital": citycare,
                "patient": arun_city,
                "doctor": city_doctor,
                "symptoms": "Occasional chest discomfort",
                "diagnosis": "Requires routine monitoring",
                "notes": "Sample development record.",
            },
        )

        MedicalRecord.objects.get_or_create(
            appointment=appointment3,
            defaults={
                "hospital": greenlife,
                "patient": anu_green,
                "doctor": green_doctor,
                "symptoms": "Mild skin irritation",
                "diagnosis": "Sample dermatology assessment",
                "notes": "Sample development record.",
            },
        )

        # 3. Prescriptions
        prescription1, _ = Prescription.objects.get_or_create(
            appointment=appointment1,
            defaults={
                "hospital": citycare,
                "patient": arun_city,
                "doctor": city_doctor,
            },
        )

        PrescriptionMedicine.objects.get_or_create(
            prescription=prescription1,
            medicine_name="Sample Medicine A",
            defaults={
                "dosage": "As prescribed",
                "frequency": "As directed",
                "duration": "5 days",
                "instructions": "Development sample only.",
            },
        )

        prescription3, _ = Prescription.objects.get_or_create(
            appointment=appointment3,
            defaults={
                "hospital": greenlife,
                "patient": anu_green,
                "doctor": green_doctor,
            },
        )

        PrescriptionMedicine.objects.get_or_create(
            prescription=prescription3,
            medicine_name="Sample Medicine B",
            defaults={
                "dosage": "As prescribed",
                "frequency": "As directed",
                "duration": "3 days",
                "instructions": "Development sample only.",
            },
        )

        # 4. Lab reports
        LabReport.objects.get_or_create(
            hospital=citycare,
            patient=arun_city,
            doctor=city_doctor,
            appointment=appointment1,
            test_name="Complete Blood Count",
            defaults={
                "test_date": today,
                "result_summary": "Sample result — not a real medical result.",
                "remarks": "Development sample only.",
            },
        )

        # Demonstrate that a lab report can exist without an appointment
        LabReport.objects.get_or_create(
            hospital=greenlife,
            patient=anu_green,
            doctor=green_doctor,
            appointment=None,
            test_name="Skin Allergy Test",
            defaults={
                "test_date": today,
                "result_summary": "Sample result — not a real medical result.",
                "remarks": "Created without an appointment for testing.",
            },
        )

        # 5. Invoices
        for appointment, fee, lab_fee, other_charges in [
            (appointment1, Decimal("500.00"), Decimal("300.00"), Decimal("50.00")),
            (appointment3, Decimal("400.00"), Decimal("0.00"), Decimal("25.00")),
        ]:
            commission_rate = appointment.doctor.op_commission_percentage
            commission = (
                fee * commission_rate / Decimal("100")
            ).quantize(Decimal("0.01"))

            Invoice.objects.get_or_create(
                appointment=appointment,
                defaults={
                    "hospital": appointment.hospital,
                    "patient": appointment.patient,
                    "consultation_fee": fee,
                    "lab_fee": lab_fee,
                    "other_charges": other_charges,
                    "total_amount": fee + lab_fee + other_charges,
                    "doctor_commission_percentage": commission_rate,
                    "doctor_commission_amount": commission,
                    "payment_status": "Pending",
                },
            )

    print("Clinical sample data created or already exists.")
    print("Appointments:", Appointment.objects.count())
    print("Medical records:", MedicalRecord.objects.count())
    print("Prescriptions:", Prescription.objects.count())
    print("Prescription medicines:", PrescriptionMedicine.objects.count())
    print("Lab reports:", LabReport.objects.count())
    print("Invoices:", Invoice.objects.count())


if __name__ == "__main__":
    seed_clinical_data()
