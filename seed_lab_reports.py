
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from platform_admin.models import (
    Hospital,
    HospitalPatient,
    Doctor,
    Appointment,
    LabReport,
)

data = [
    {
        "hospital": "City Care Hospital",
        "patient": "patient.arun",
        "doctor": "doctor.citycare1",
        "reason": "Routine heart checkup",
        "test_name": "Test ECG Report",
        "result_summary": "Fictional ECG result for software testing",
        "remarks": "Sample report only",
        "with_appointment": True,
    },
    {
        "hospital": "City Care Hospital",
        "patient": "patient.arun",
        "doctor": "doctor.citycare1",
        "reason": "Routine heart checkup",
        "test_name": "Test Blood Report",
        "result_summary": "Fictional blood test result for software testing",
        "remarks": "Second report for the same appointment",
        "with_appointment": True,
    },
    {
        "hospital": "Green Life Hospital",
        "patient": "patient.anu",
        "doctor": "doctor.greenlife1",
        "reason": None,
        "test_name": "Test Skin Investigation",
        "result_summary": "Fictional result for software testing",
        "remarks": "Report created without an appointment",
        "with_appointment": False,
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

    appointment = None

    if item["with_appointment"]:
        appointment = Appointment.objects.filter(
            hospital=hospital,
            patient=registration,
            doctor=doctor,
            reason=item["reason"],
        ).order_by("-date", "-time").first()

        if appointment is None:
            print(f"Skipped: appointment not found for {item['patient']}")
            continue

    report, created = LabReport.objects.get_or_create(
        hospital=hospital,
        patient=registration,
        doctor=doctor,
        appointment=appointment,
        test_name=item["test_name"],
        defaults={
            "result_summary": item["result_summary"],
            "remarks": item["remarks"],
        },
    )

    print(
        f"{hospital.name} | {report.test_name} | "
        f"{'Created' if created else 'Already exists'}"
    )
