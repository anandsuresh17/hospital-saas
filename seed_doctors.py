
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.contrib.auth.models import User
from platform_admin.models import Hospital, Department, Doctor

data = [
    {
        "username": "doctor.citycare1",
        "email": "doctor.citycare1@example.com",
        "hospital": "City Care Hospital",
        "department": "Cardiology",
        "specialization": "Cardiology",
        "qualification": "MBBS, MD",
        "experience_years": 8,
        "consultation_fee": 500,
        "op_commission_percentage": 10,
        "contact_number": "9000000021",
    },
    {
        "username": "doctor.metro1",
        "email": "doctor.metro1@example.com",
        "hospital": "Metro Medical Centre",
        "department": "Neurology",
        "specialization": "Neurology",
        "qualification": "MBBS, DM",
        "experience_years": 10,
        "consultation_fee": 700,
        "op_commission_percentage": 12,
        "contact_number": "9000000022",
    },
    {
        "username": "doctor.greenlife1",
        "email": "doctor.greenlife1@example.com",
        "hospital": "Green Life Hospital",
        "department": "Dermatology",
        "specialization": "Dermatology",
        "qualification": "MBBS, MD",
        "experience_years": 6,
        "consultation_fee": 400,
        "op_commission_percentage": 10,
        "contact_number": "9000000023",
    },
]

for item in data:
    hospital = Hospital.objects.get(name=item["hospital"])
    department = Department.objects.get(
        hospital=hospital,
        name=item["department"],
    )

    user, user_created = User.objects.get_or_create(
        username=item["username"],
        defaults={"email": item["email"]},
    )

    if user_created:
        user.set_password("Doctor@Dev2026!")
        user.save()

    doctor, doctor_created = Doctor.objects.get_or_create(
        user=user,
        defaults={
            "hospital": hospital,
            "department": department,
            "specialization": item["specialization"],
            "qualification": item["qualification"],
            "experience_years": item["experience_years"],
            "consultation_fee": item["consultation_fee"],
            "op_commission_percentage": item["op_commission_percentage"],
            "contact_number": item["contact_number"],
        },
    )

    if not doctor_created and (
        doctor.hospital_id != hospital.id
        or doctor.department_id != department.id
    ):
        print(f"Warning: {user.username} is linked to different details.")
        continue

    print(
        f"{user.username}: "
        f"{'Created' if doctor_created else 'Already exists'} "
        f"| {hospital.name} | {department.name}"
    )
