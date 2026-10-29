
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from platform_admin.models import Hospital, Department

data = {
    "City Care Hospital": [
        "Cardiology",
        "Orthopedics",
        "General Medicine",
    ],
    "Metro Medical Centre": [
        "Cardiology",
        "Neurology",
        "Pediatrics",
    ],
    "Green Life Hospital": [
        "General Medicine",
        "Dermatology",
        "Orthopedics",
    ],
}

for hospital_name, department_names in data.items():
    hospital = Hospital.objects.get(name=hospital_name)

    for department_name in department_names:
        department, created = Department.objects.get_or_create(
            hospital=hospital,
            name=department_name,
            defaults={
                "description": f"{department_name} department at {hospital.name}",
                "is_active": True,
            },
        )

        status = "Created" if created else "Already exists"
        print(f"{hospital.name} - {department.name}: {status}")
