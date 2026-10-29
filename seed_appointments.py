
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from datetime import date, time, timedelta
from platform_admin.models import (
    Hospital,
    HospitalPatient,
    Doctor,
    Department,
    Appointment,
)

today = date.today()

data = [
    {
        "hospital": "City Care Hospital",
        "patient": "patient.arun",
        "doctor": "doctor.citycare1",
        "department": "Cardiology",
        "days": 1,
        "time": time(10, 0),
        "reason": "Routine heart checkup",
        "status": "Pending",
    },
    {
        "hospital": "Metro Medical Centre",
        "patient": "patient.arun",
        "doctor": "doctor.metro1",
        "department": "Neurology",
        "days": 2,
        "time": time(11, 0),
        "reason": "Headache consultation",
        "status": "Confirmed",
    },
    {
        "hospital": "Green Life Hospital",
        "patient": "patient.anu",
        "doctor": "doctor.greenlife1",
        "department": "Dermatology",
        "days": 3,
        "time": time(14, 0),
        "reason": "Skin consultation",
        "status": "Pending",
    },
]

for item in data:
    hospital = Hospital.objects.get(name=item["hospital"])

    registration = HospitalPatient.objects.get(
        hospital=hospital,
        patient__user__username=item["patient"],
    )

    doctor = Doctor.objects.get(
        user__username=item["doctor"],
        hospital=hospital,
    )

    department = Department.objects.get(
        hospital=hospital,
        name=item["department"],
    )

    appointment_date = today + timedelta(days=item["days"])

    appointment, created = Appointment.objects.get_or_create(
        hospital=hospital,
        patient=registration,
        doctor=doctor,
        department=department,
        date=appointment_date,
        time=item["time"],
        defaults={
            "reason": item["reason"],
            "status": item["status"],
        },
    )

    print(
        f"{hospital.name} | {item['patient']} | "
        f"{appointment.date} | "
        f"{'Created' if created else 'Already exists'}"
    )
