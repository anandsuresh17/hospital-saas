
from django import forms
from .models import Hospital, SubscriptionPlan, HospitalTemplate,Hospital


# Hospital Form
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["subscription_plan"].queryset = (
            SubscriptionPlan.objects.filter(is_active=True)
        )

        if self.instance and self.instance.pk:
            current_plan = self.instance.subscription_plan

            self.fields["subscription_plan"].queryset |= (
                SubscriptionPlan.objects.filter(pk=current_plan.pk)
            )

        self.fields["template"].queryset = (
            HospitalTemplate.objects.filter(is_active=True)
        )

        if self.instance and self.instance.pk:
            current_template = self.instance.template

            self.fields["template"].queryset |= (
                HospitalTemplate.objects.filter(pk=current_template.pk)
            )


# Subscription Plan Form
class SubscriptionPlanForm(forms.ModelForm):

    class Meta:
        model = SubscriptionPlan
        fields = [
            "name",
            "price",
            "duration_days",
            "description",
            "features",
            "is_active",
        ]


# Hospital Template Form
class HospitalTemplateForm(forms.ModelForm):

    class Meta:
        model = HospitalTemplate
        fields = [
            "name",
            "template_key",
            "description",
            "template_path",
            "preview_image",
            "is_active",
        ]




class HospitalWebsiteForm(forms.ModelForm):

    class Meta:
        model = Hospital

        fields = [
            'name',
            'email',
            'contact_number',
            'address',
            'website',
            'tagline',
            'about',
            'logo',
            'banner',
            'working_hours',
            'facebook_url',
            'instagram_url',
            'template',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter hospital name',
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter hospital email',
            }),

            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact number',
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter hospital address',
            }),

            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
            }),

            'tagline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter hospital tagline',
            }),

            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write about your hospital',
            }),

            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),

            'banner': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),

            'working_hours': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Monday - Saturday: 9 AM - 6 PM',
            }),

            'facebook_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Facebook URL',
            }),

            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Instagram URL',
            }),

            'template': forms.Select(attrs={
                'class': 'form-select',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['template'].queryset = (
            self.fields['template'].queryset.filter(is_active=True)
        )