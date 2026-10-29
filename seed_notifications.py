
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from django.contrib.auth.models import User
from platform_admin.models import Notification

data = [
    {
        "username": "citycare_admin",
        "title": "New patient registration",
        "message": "A test patient has registered at your hospital.",
    },
    {
        "username": "doctor.citycare1",
        "title": "Upcoming appointment",
        "message": "You have a test appointment scheduled.",
    },
    {
        "username": "receptionist.citycare",
        "title": "Appointment update",
        "message": "A test appointment requires your attention.",
    },
    {
        "username": "patient.arun",
        "title": "Appointment confirmation",
        "message": "Your test appointment has been confirmed.",
    },
]

for item in data:
    user = User.objects.filter(
        username=item["username"]
    ).first()

    if user is None:
        print(f"Skipped: user '{item['username']}' does not exist")
        continue

    notification, created = Notification.objects.get_or_create(
        user=user,
        title=item["title"],
        defaults={
            "message": item["message"],
            "is_read": False,
        },
    )

    status = "Created" if created else "Already exists"
    print(f"{user.username} | {notification.title} | {status}")
