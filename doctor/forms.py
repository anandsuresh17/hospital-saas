
from django import forms
from platform_admin.models import MedicalRecord


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
            'patient': forms.Select(attrs={
                'class': 'form-select'
            }),
            'appointment': forms.Select(attrs={
                'class': 'form-select'
            }),
            'symptoms': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'diagnosis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
        }
