
import os
import django
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from platform_admin.models import (
    Hospital,
    HospitalPatient,
    Doctor,
    Appointment,
    Invoice,
)

data = [
    {
        "hospital": "City Care Hospital",
        "patient": "patient.arun",
        "doctor": "doctor.citycare1",
        "reason": "Routine heart checkup",
        "lab_fee": Decimal("300.00"),
        "other_charges": Decimal("100.00"),
        "payment_status": "Pending",
    },
    {
        "hospital": "Metro Medical Centre",
        "patient": "patient.arun",
        "doctor": "doctor.metro1",
        "reason": "Headache consultation",
        "lab_fee": Decimal("500.00"),
        "other_charges": Decimal("150.00"),
        "payment_status": "Paid",
    },
    {
        "hospital": "Green Life Hospital",
        "patient": "patient.anu",
        "doctor": "doctor.greenlife1",
        "reason": "Skin consultation",
        "lab_fee": Decimal("200.00"),
        "other_charges": Decimal("50.00"),
        "payment_status": "Pending",
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

    consultation_fee = Decimal(str(doctor.consultation_fee))
    commission_percentage = Decimal(
        str(doctor.op_commission_percentage)
    )

    commission_amount = (
        consultation_fee * commission_percentage / Decimal("100")
    ).quantize(Decimal("0.01"))

    total_amount = (
        consultation_fee
        + item["lab_fee"]
        + item["other_charges"]
    )

    invoice, created = Invoice.objects.get_or_create(
        appointment=appointment,
        defaults={
            "hospital": hospital,
            "patient": registration,
            "consultation_fee": consultation_fee,
            "lab_fee": item["lab_fee"],
            "other_charges": item["other_charges"],
            "total_amount": total_amount,
            "doctor_commission_percentage": commission_percentage,
            "doctor_commission_amount": commission_amount,
            "payment_status": item["payment_status"],
        },
    )

    print(
        f"{hospital.name} | Invoice #{invoice.pk} | "
        f"Total: {invoice.total_amount} | "
        f"{'Created' if created else 'Already exists'}"
    )
