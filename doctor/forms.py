
from django import forms
from django.forms import inlineformset_factory

from platform_admin.models import (
    MedicalRecord,
    Prescription,
    PrescriptionMedicine,
    LabReport,
)


# ==========================================
# 1. MEDICAL RECORD FORM
# ==========================================

class MedicalRecordForm(forms.ModelForm):

    class Meta:
        model = MedicalRecord
        fields = [
            'patient',
            'appointment',
            'symptoms',
            'diagnosis',
            'notes',
        ]

        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'appointment': forms.Select(attrs={'class': 'form-select'}),
            'symptoms': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3
            }),
            'diagnosis': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3
            }),
        }


# ==========================================
# 2. PRESCRIPTION MEDICINE FORM
# ==========================================

class PrescriptionMedicineForm(forms.ModelForm):

    class Meta:
        model = PrescriptionMedicine
        fields = [
            'medicine_name',
            'dosage',
            'frequency',
            'duration',
            'instructions',
        ]

        widgets = {
            'medicine_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Medicine name'
            }),
            'dosage': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 500 mg'
            }),
            'frequency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Twice daily'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 5 days'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }


# ==========================================
# 3. PRESCRIPTION MEDICINE FORMSET
# ==========================================

PrescriptionMedicineFormSet = inlineformset_factory(
    Prescription,
    PrescriptionMedicine,
    form=PrescriptionMedicineForm,
    extra=1,
    can_delete=True,
)


# ==========================================
# 4. LAB REPORT FORM
# ==========================================

class LabReportForm(forms.ModelForm):

    class Meta:
        model = LabReport

        fields = [
            'patient',
            'appointment',
            'test_name',
            'test_date',
            'result_summary',
            'report_file',
            'remarks',
        ]

        widgets = {
            'patient': forms.Select(attrs={
                'class': 'form-select'
            }),

            'appointment': forms.Select(attrs={
                'class': 'form-select'
            }),

            'test_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter test name'
            }),

            'test_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'result_summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),

            'report_file': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
