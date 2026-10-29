
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.contrib.auth.models import User
from platform_admin.models import Hospital, HospitalAdmin

data = [
    {
        "hospital_email": "citycare@example.com",
        "username": "citycare_admin",
        "email": "admin.citycare@example.com",
        "password": "CityCare@Dev2026!",
        "phone": "9000000011",
    },
    {
        "hospital_email": "metro@example.com",
        "username": "metro_admin",
        "email": "admin.metro@example.com",
        "password": "Metro@Dev2026!",
        "phone": "9000000012",
    },
    {
        "hospital_email": "greenlife@example.com",
        "username": "greenlife_admin",
        "email": "admin.greenlife@example.com",
        "password": "GreenLife@Dev2026!",
        "phone": "9000000013",
    },
]

for item in data:
    hospital = Hospital.objects.get(email=item["hospital_email"])

    user, user_created = User.objects.get_or_create(
        username=item["username"],
        defaults={"email": item["email"]},
    )

    if user_created:
        user.set_password(item["password"])
        user.save()
    elif not user.has_usable_password():
        user.set_password(item["password"])
        user.save()

    if user.email != item["email"]:
        print(f"Warning: {item['username']} has a different email already.")

    profile, profile_created = HospitalAdmin.objects.get_or_create(
        user=user,
        defaults={
            "hospital": hospital,
            "contact_number": item["phone"],
        },
    )

    if not profile_created and profile.hospital_id != hospital.id:
        print(f"Warning: {item['username']} is linked to another hospital.")
        continue

    status = "Created" if user_created else "User already exists"
    print(f"{item['username']}: {status} | {hospital.name}")
