from django.contrib import admin
from .models import (
    HospitalTemplate,
    SubscriptionPlan,
    Role,
    Hospital,
    HospitalAdmin,
    Department,
    Doctor,
    Patient,
    HospitalPatient,
    Receptionist,
    Appointment,
    MedicalRecord,
    Prescription,
    PrescriptionMedicine,
    LabReport,
    Invoice,
    Notification,
)


@admin.register(HospitalTemplate)
class HospitalTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "template_key", "is_active", "created_at")
    search_fields = ("name", "template_key")
    list_filter = ("is_active",)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "duration_days", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Hospital)
class HospitalAdminPanel(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "contact_number",
        "template",
        "subscription_plan",
        "is_active",
    )
    search_fields = ("name", "email", "contact_number")
    list_filter = ("is_active", "template", "subscription_plan")


@admin.register(HospitalAdmin)
class HospitalAdminUserAdmin(admin.ModelAdmin):
    list_display = ("user", "hospital", "contact_number", "created_at")
    search_fields = ("user__username", "user__email", "hospital__name")
    list_filter = ("hospital",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "hospital", "is_active", "created_at")
    search_fields = ("name", "hospital__name")
    list_filter = ("hospital", "is_active")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "hospital",
        "department",
        "specialization",
        "consultation_fee",
        "experience_years",
    )
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "specialization",
    )
    list_filter = ("hospital", "department")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "gender",
        "contact_number",
        "blood_group",
    )
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "contact_number",
    )
    list_filter = ("gender", "blood_group")


@admin.register(HospitalPatient)
class HospitalPatientAdmin(admin.ModelAdmin):
    list_display = (
        "patient_id_code",
        "hospital",
        "patient",
        "registered_at",
    )
    search_fields = (
        "patient_id_code",
        "hospital__name",
        "patient__user__username",
        "patient__user__email",
    )
    list_filter = ("hospital", "registered_at")


@admin.register(Receptionist)
class ReceptionistAdmin(admin.ModelAdmin):
    list_display = ("user", "hospital", "contact_number", "created_at")
    search_fields = ("user__username", "user__email", "hospital__name")
    list_filter = ("hospital",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hospital",
        "patient",
        "doctor",
        "department",
        "date",
        "time",
        "status",
    )
    search_fields = (
        "patient__patient_id_code",
        "patient__patient__user__username",
        "doctor__user__username",
        "hospital__name",
    )
    list_filter = ("hospital", "department", "status", "date")
    date_hierarchy = "date"


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hospital",
        "patient",
        "doctor",
        "appointment",
        "created_at",
    )
    search_fields = (
        "patient__patient_id_code",
        "patient__patient__user__username",
        "doctor__user__username",
    )
    list_filter = ("hospital", "created_at")


class PrescriptionMedicineInline(admin.TabularInline):
    model = PrescriptionMedicine
    extra = 1


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hospital",
        "patient",
        "doctor",
        "appointment",
        "created_at",
    )
    search_fields = (
        "patient__patient_id_code",
        "patient__patient__user__username",
        "doctor__user__username",
    )
    list_filter = ("hospital", "created_at")
    inlines = [PrescriptionMedicineInline]


@admin.register(PrescriptionMedicine)
class PrescriptionMedicineAdmin(admin.ModelAdmin):
    list_display = (
        "medicine_name",
        "prescription",
        "dosage",
        "frequency",
        "duration",
    )
    search_fields = ("medicine_name",)
    list_filter = ("frequency",)


@admin.register(LabReport)
class LabReportAdmin(admin.ModelAdmin):
    list_display = (
        "test_name",
        "hospital",
        "patient",
        "doctor",
        "test_date",
    )
    search_fields = (
        "test_name",
        "patient__patient_id_code",
        "patient__patient__user__username",
        "doctor__user__username",
    )
    list_filter = ("hospital", "test_date")


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hospital",
        "patient",
        "appointment",
        "total_amount",
        "payment_status",
        "created_at",
    )
    search_fields = (
        "patient__patient_id_code",
        "patient__patient__user__username",
    )
    list_filter = ("hospital", "payment_status", "created_at")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "is_read", "created_at")
    search_fields = ("title", "message", "user__username", "user__email")
    list_filter = ("is_read", "created_at")