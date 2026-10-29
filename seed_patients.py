
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from datetime import date
from django.contrib.auth.models import User
from platform_admin.models import Patient, Hospital, HospitalPatient

data = [
    {
        "username": "patient.arun",
        "email": "arun.patient@example.com",
        "first_name": "Arun",
        "last_name": "Kumar",
        "dob": date(1998, 5, 12),
        "gender": "Male",
        "phone": "9000000041",
        "address": "Kochi, Kerala",
        "blood_group": "O+",
        "emergency_contact": "9000000042",
        "hospitals": [
            "City Care Hospital",
            "Metro Medical Centre",
        ],
    },
    {
        "username": "patient.anu",
        "email": "anu.patient@example.com",
        "first_name": "Anu",
        "last_name": "Thomas",
        "dob": date(2000, 8, 20),
        "gender": "Female",
        "phone": "9000000043",
        "address": "Thrissur, Kerala",
        "blood_group": "A+",
        "emergency_contact": "9000000044",
        "hospitals": ["Green Life Hospital"],
    },
]

for item in data:
    user, user_created = User.objects.get_or_create(
        username=item["username"],
        defaults={
            "email": item["email"],
            "first_name": item["first_name"],
            "last_name": item["last_name"],
        },
    )

    if user_created:
        user.set_password("Patient@Dev2026!")
        user.save()

    patient, patient_created = Patient.objects.get_or_create(
        user=user,
        defaults={
            "date_of_birth": item["dob"],
            "gender": item["gender"],
            "contact_number": item["phone"],
            "address": item["address"],
            "blood_group": item["blood_group"],
            "emergency_contact": item["emergency_contact"],
        },
    )

    for hospital_name in item["hospitals"]:
        hospital = Hospital.objects.get(name=hospital_name)

        registration, created = HospitalPatient.objects.get_or_create(
            hospital=hospital,
            patient=patient,
            defaults={
                "patient_id_code": (
                    f"H{hospital.id}-P{patient.id}"
                ),
            },
        )

        print(
            f"{patient.user.username} | {hospital.name} | "
            f"{'Registered' if created else 'Already registered'}"
        )

    print(f"Patient profile ready: {patient.user.username}")
