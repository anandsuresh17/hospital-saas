
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.contrib.auth.models import User
from platform_admin.models import Hospital, Receptionist

data = [
    {
        "username": "receptionist.citycare",
        "email": "receptionist.citycare@example.com",
        "hospital": "City Care Hospital",
        "phone": "9000000031",
    },
    {
        "username": "receptionist.metro",
        "email": "receptionist.metro@example.com",
        "hospital": "Metro Medical Centre",
        "phone": "9000000032",
    },
    {
        "username": "receptionist.greenlife",
        "email": "receptionist.greenlife@example.com",
        "hospital": "Green Life Hospital",
        "phone": "9000000033",
    },
]

for item in data:
    hospital = Hospital.objects.get(name=item["hospital"])

    user, user_created = User.objects.get_or_create(
        username=item["username"],
        defaults={"email": item["email"]},
    )

    if user_created:
        user.set_password("Reception@Dev2026!")
        user.save()

    receptionist, profile_created = Receptionist.objects.get_or_create(
        user=user,
        defaults={
            "hospital": hospital,
            "contact_number": item["phone"],
        },
    )

    if not profile_created and receptionist.hospital_id != hospital.id:
        print(f"Warning: {user.username} is linked to another hospital.")
        continue

    status = "Created" if profile_created else "Already exists"
    print(f"{user.username}: {status} | {hospital.name}")
