
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from platform_admin.models import (
    Hospital,
    HospitalPatient,
    Doctor,
    Appointment,
    Prescription,
    PrescriptionMedicine,
)

data = [
    {
        "hospital": "City Care Hospital",
        "patient": "patient.arun",
        "doctor": "doctor.citycare1",
        "reason": "Routine heart checkup",
        "medicines": [
            {
                "name": "Test Medicine A",
                "dosage": "As prescribed",
                "frequency": "Twice daily",
                "duration": "3 days",
                "instructions": "Fictional test data only",
            },
            {
                "name": "Test Medicine B",
                "dosage": "As prescribed",
                "frequency": "Once daily",
                "duration": "5 days",
                "instructions": "Fictional test data only",
            },
        ],
    },
    {
        "hospital": "Metro Medical Centre",
        "patient": "patient.arun",
        "doctor": "doctor.metro1",
        "reason": "Headache consultation",
        "medicines": [
            {
                "name": "Test Medicine C",
                "dosage": "As prescribed",
                "frequency": "Once daily",
                "duration": "2 days",
                "instructions": "Fictional test data only",
            },
        ],
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
        print(f"Skipped: appointment not found for {item['patient']}")
        continue

    prescription, created = Prescription.objects.get_or_create(
        appointment=appointment,
        defaults={
            "hospital": hospital,
            "patient": registration,
            "doctor": doctor,
        },
    )

    if created:
        for medicine in item["medicines"]:
            PrescriptionMedicine.objects.create(
                prescription=prescription,
                medicine_name=medicine["name"],
                dosage=medicine["dosage"],
                frequency=medicine["frequency"],
                duration=medicine["duration"],
                instructions=medicine["instructions"],
            )

    print(
        f"{hospital.name} | "
        f"{'Created' if created else 'Already exists'}"
    )
