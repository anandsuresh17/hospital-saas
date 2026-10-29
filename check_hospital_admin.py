
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from platform_admin.models import HospitalAdmin

for field in HospitalAdmin._meta.fields:
    print(field.name, field.get_internal_type())
