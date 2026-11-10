
from django import forms
from django.contrib.auth.models import User

from platform_admin.models import (
    Department,
    Doctor,
    Receptionist,
    Patient,
)


# =====================================
# DEPARTMENT FORM
# =====================================

class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = [
            'name',
            'description',
            'is_active'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter department name'
            }),

            'description': forms.Textarea(attrs={
                'placeholder': 'Enter department description',
                'rows': 3
            }),
        }


# =====================================
# DOCTOR CREATE FORM
# =====================================

class DoctorCreateForm(forms.Form):

    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.none()
    )

    qualification = forms.CharField(max_length=150)

    specialization = forms.CharField(
        max_length=150,
        required=False
    )

    experience_years = forms.IntegerField(
        min_value=0,
        initial=0
    )

    consultation_fee = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0
    )

    op_commission_percentage = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        initial=0
    )

    contact_number = forms.CharField(
        max_length=20,
        required=False
    )

    available_days = forms.CharField(
        max_length=200,
        required=False
    )

    available_time_start = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    available_time_end = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    def __init__(self, *args, hospital=None, **kwargs):
        super().__init__(*args, **kwargs)

        if hospital:
            self.fields['department'].queryset = Department.objects.filter(
                hospital=hospital,
                is_active=True
            )

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username already exists."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email already exists."
            )

        return email


# =====================================
# DOCTOR UPDATE FORM
# =====================================

class DoctorUpdateForm(forms.ModelForm):

    class Meta:
        model = Doctor

        fields = [
            'department',
            'qualification',
            'specialization',
            'experience_years',
            'consultation_fee',
            'op_commission_percentage',
            'contact_number',
            'available_days',
            'available_time_start',
            'available_time_end',
        ]

        widgets = {
            'available_time_start': forms.TimeInput(
                attrs={'type': 'time'}
            ),

            'available_time_end': forms.TimeInput(
                attrs={'type': 'time'}
            ),
        }

    def __init__(self, *args, hospital=None, **kwargs):
        super().__init__(*args, **kwargs)

        if hospital:
            departments = Department.objects.filter(
                hospital=hospital,
                is_active=True
            )

            if self.instance and self.instance.pk:
                departments = departments | Department.objects.filter(
                    pk=self.instance.department_id,
                    hospital=hospital
                )

            self.fields['department'].queryset = departments.distinct()


# =====================================
# RECEPTIONIST CREATE FORM
# =====================================

class ReceptionistCreateForm(forms.ModelForm):

    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = Receptionist
        fields = ['contact_number']

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username already exists."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email already exists."
            )

        return email


# =====================================
# RECEPTIONIST UPDATE FORM
# =====================================

class ReceptionistUpdateForm(forms.ModelForm):

    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = Receptionist
        fields = ['contact_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def clean_username(self):
        username = self.cleaned_data['username']

        existing_users = User.objects.filter(
            username=username
        ).exclude(
            pk=self.instance.user_id
        )

        if existing_users.exists():
            raise forms.ValidationError(
                "This username is already in use."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        existing_users = User.objects.filter(
            email__iexact=email
        ).exclude(
            pk=self.instance.user_id
        )

        if existing_users.exists():
            raise forms.ValidationError(
                "This email is already in use."
            )

        return email


# =====================================
# PATIENT UPDATE FORM
# =====================================

class PatientUpdateForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=150,
        required=False
    )

    last_name = forms.CharField(
        max_length=150,
        required=False
    )

    email = forms.EmailField(
        required=False
    )

    class Meta:
        model = Patient

        fields = [
            'date_of_birth',
            'gender',
            'contact_number',
            'address',
            'blood_group',
            'emergency_contact',
        ]

        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'address': forms.Textarea(
                attrs={'rows': 3}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = (
                self.instance.user.first_name
            )

            self.fields['last_name'].initial = (
                self.instance.user.last_name
            )

            self.fields['email'].initial = (
                self.instance.user.email
            )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email:
            existing_users = User.objects.filter(
                email__iexact=email
            ).exclude(
                pk=self.instance.user_id
            )

            if existing_users.exists():
                raise forms.ValidationError(
                    "This email is already in use."
                )

        return email
