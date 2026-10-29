
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.contrib.auth.models import User
from django.db import transaction
from platform_admin.models import (
    Hospital,
    Department,
    Doctor,
    Receptionist,
    Patient,
    HospitalPatient,
)


def get_user(username, email, password):
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email},
    )

    if created:
        user.set_password(password)
        user.save()

    return user


@transaction.atomic
def seed_people():
    # Create one doctor for each hospital.
    doctors = [
        {
            "username": "doctor.citycare1",
            "email": "doctor.citycare1@example.com",
            "password": "Doctor@Dev2026!",
            "hospital": "City Care Hospital",
            "department": "Cardiology",
            "specialization": "Cardiology",
            "qualification": "MBBS, MD",
            "experience_years": 8,
            "consultation_fee": 500,
            "op_commission_percentage": 10,
            "phone": "9000000021",
        },
        {
            "username": "doctor.metro1",
            "email": "doctor.metro1@example.com",
            "password": "Doctor@Dev2026!",
            "hospital": "Metro Medical Centre",
            "department": "Neurology",
            "specialization": "Neurology",
            "qualification": "MBBS, DM",
            "experience_years": 10,
            "consultation_fee": 700,
            "op_commission_percentage": 12,
            "phone": "9000000022",
        },
        {
            "username": "doctor.greenlife1",
            "email": "doctor.greenlife1@example.com",
            "password": "Doctor@Dev2026!",
            "hospital": "Green Life Hospital",
            "department": "Dermatology",
            "specialization": "Dermatology",
            "qualification": "MBBS, MD",
            "experience_years": 6,
            "consultation_fee": 400,
            "op_commission_percentage": 10,
            "phone": "9000000023",
        },
    ]

    for item in doctors:
        hospital = Hospital.objects.get(name=item["hospital"])
        department = Department.objects.get(
            hospital=hospital,
            name=item["department"],
        )

        user = get_user(
            item["username"], item["email"], item["password"]
        )

        doctor, created = Doctor.objects.get_or_create(
            user=user,
            defaults={
                "hospital": hospital,
                "department": department,
                "specialization": item["specialization"],
                "qualification": item["qualification"],
                "experience_years": item["experience_years"],
                "consultation_fee": item["consultation_fee"],
                "op_commission_percentage": item[
                    "op_commission_percentage"
                ],
                "contact_number": item["phone"],
            },
        )

        if not created and (
            doctor.hospital_id != hospital.id
            or doctor.department_id != department.id
        ):
            raise ValueError(
                f"{user.username} already has a different doctor profile."
            )

        print(f"Doctor ready: {user.username}")

    # Create one receptionist for each hospital.
    receptionists = [
        ("receptionist.citycare", "City Care Hospital", "9000000031"),
        ("receptionist.metro", "Metro Medical Centre", "9000000032"),
        ("receptionist.greenlife", "Green Life Hospital", "9000000033"),
    ]

    for username, hospital_name, phone in receptionists:
        hospital = Hospital.objects.get(name=hospital_name)
        user = get_user(
            username,
            f"{username}@example.com",
            "Reception@Dev2026!",
        )

        profile, created = Receptionist.objects.get_or_create(
            user=user,
            defaults={
                "hospital": hospital,
                "contact_number": phone,
            },
        )

        if not created and profile.hospital_id != hospital.id:
            raise ValueError(
                f"{username} is linked to a different hospital."
            )

        print(f"Receptionist ready: {username}")

    # Create two patients and their hospital registrations.
    patients = [
        {
            "username": "patient.arun",
            "email": "arun.patient@example.com",
            "first_name": "Arun",
            "last_name": "Kumar",
            "dob": "1998-05-12",
            "gender": "Male",
            "phone": "9000000041",
            "address": "Kochi, Kerala",
            "blood_group": "O+",
            "emergency_contact": "9000000042",
            "hospitals": ["City Care Hospital", "Metro Medical Centre"],
        },
        {
            "username": "patient.anu",
            "email": "anu.patient@example.com",
            "first_name": "Anu",
            "last_name": "Thomas",
            "dob": "2000-08-20",
            "gender": "Female",
            "phone": "9000000043",
            "address": "Thrissur, Kerala",
            "blood_group": "A+",
            "emergency_contact": "9000000044",
            "hospitals": ["Green Life Hospital"],
        },
    ]

    from datetime import date

    for item in patients:
        user = get_user(
            item["username"],
            item["email"],
            "Patient@Dev2026!",
        )

        if not user.first_name and not user.last_name:
            user.first_name = item["first_name"]
            user.last_name = item["last_name"]
            user.save()

        patient, created = Patient.objects.get_or_create(
            user=user,
            defaults={
                "date_of_birth": date.fromisoformat(item["dob"]),
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
                    "patient_id_code": f"H{hospital.id}-P{patient.id}",
                },
            )

            print(
                f"Registration ready: {user.username} | "
                f"{hospital.name}"
            )

        print(f"Patient ready: {user.username}")


if __name__ == "__main__":
    seed_people()
