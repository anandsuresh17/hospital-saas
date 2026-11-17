
from django import forms
from django.contrib.auth.models import User

from platform_admin.models import (
    Department,
    Doctor,
    Receptionist,
    Patient,
    SubscriptionPlan,
    SubscriptionRequest,
)


# =====================================
# DEPARTMENT FORM
# =====================================

class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter department name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter department description'
            }),
        }


# =====================================
# DOCTOR CREATE FORM
# =====================================

class DoctorCreateForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter first name'
        })
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter last name'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

    contact_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter contact number'
        })
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.none(),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    def __init__(self, *args, **kwargs):
        hospital = kwargs.pop('hospital')
        super().__init__(*args, **kwargs)

        self.fields['department'].queryset = Department.objects.filter(
            hospital=hospital
        )

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists.')

        return email


# =====================================
# DOCTOR UPDATE FORM
# =====================================

class DoctorUpdateForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Doctor
        fields = ['department', 'contact_number']

        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }


# =====================================
# RECEPTIONIST CREATE FORM
# =====================================

class ReceptionistCreateForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    contact_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists.')

        return email


# =====================================
# RECEPTIONIST UPDATE FORM
# =====================================

class ReceptionistUpdateForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Receptionist
        fields = ['contact_number']

        widgets = {
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }


# =====================================
# PATIENT UPDATE FORM
# =====================================

class PatientUpdateForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['contact_number', 'address']

        widgets = {
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


# =====================================
# SUBSCRIPTION REQUEST FORM
# =====================================

class SubscriptionRequestForm(forms.ModelForm):

    class Meta:
        model = SubscriptionRequest

        fields = [
            'requested_plan',
            'message',
        ]

        widgets = {
            'requested_plan': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Explain why you want to change your subscription plan...'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['requested_plan'].queryset = (
            SubscriptionPlan.objects.filter(is_active=True)
        )
