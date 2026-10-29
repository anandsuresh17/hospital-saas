
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from platform_admin.models import Hospital, SubscriptionPlan, HospitalTemplate

data = [
    ("City Care Hospital", "citycare@example.com", "9000000001",
     "MG Road, Kochi, Kerala", "Basic", "Modern"),
    ("Metro Medical Centre", "metro@example.com", "9000000002",
     "Technopark Road, Thiruvananthapuram, Kerala", "Standard", "Classic"),
    ("Green Life Hospital", "greenlife@example.com", "9000000003",
     "Thrissur, Kerala", "Premium", "Multispecialty"),
]

for name, email, phone, address, plan_name, template_name in data:
    plan = SubscriptionPlan.objects.get(name=plan_name)
    template = HospitalTemplate.objects.get(name=template_name)

    hospital, created = Hospital.objects.get_or_create(
        email=email,
        defaults={
            "name": name,
            "contact_number": phone,
            "address": address,
            "website": "",
            "subscription_plan": plan,
            "template": template,
            "is_active": True,
        },
    )

    print(f"{hospital.name}: {'Created' if created else 'Already exists'}")
