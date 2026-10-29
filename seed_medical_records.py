
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from platform_admin.models import (
    Hospital,
    HospitalPatient,
    Doctor,
    Appointment,
    MedicalRecord,
)

data = [
    {
        "hospital": "City Care Hospital",
        "patient": "patient.arun",
        "doctor": "doctor.citycare1",
        "reason": "Routine heart checkup",
        "symptoms": "Occasional chest discomfort",
        "diagnosis": "Requires routine cardiac evaluation",
        "notes": "Fictional test record. Follow-up recommended.",
    },
    {
        "hospital": "Metro Medical Centre",
        "patient": "patient.arun",
        "doctor": "doctor.metro1",
        "reason": "Headache consultation",
        "symptoms": "Recurring headaches",
        "diagnosis": "Assessment required for recurring headache",
        "notes": "Fictional test record. Review symptoms at follow-up.",
    },
]

for item in data:
    hospital = Hospital.objects.get(name=item["hospital"])

    registration = HospitalPatient.objects.get(
        hospital=hospital,
        patient__user__username=item["patient"],
    )

    doctor = Doctor.objects.get(
        hospital=hospital,
        user__username=item["doctor"],
    )

    appointment = Appointment.objects.filter(
        hospital=hospital,
        patient=registration,
        doctor=doctor,
        reason=item["reason"],
    ).order_by("-date", "-time").first()

    if appointment is None:
        print(f"Skipped: no appointment found for {item['patient']}")
        continue

    record, created = MedicalRecord.objects.get_or_create(
        appointment=appointment,
        defaults={
            "hospital": hospital,
            "patient": registration,
            "doctor": doctor,
            "symptoms": item["symptoms"],
            "diagnosis": item["diagnosis"],
            "notes": item["notes"],
        },
    )

    print(
        f"{hospital.name} | {item['patient']} | "
        f"{'Created' if created else 'Already exists'}"
    )
