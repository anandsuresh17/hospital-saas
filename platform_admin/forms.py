
from django import forms
from .models import Hospital


class HospitalForm(forms.ModelForm):

    class Meta:
        model = Hospital
        fields = [
            "name",
            "email",
            "contact_number",
            "address",
            "website",
            "template",
            "subscription_plan",
            "is_active",
        ]
