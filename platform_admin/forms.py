
from django import forms
from .models import Hospital, SubscriptionPlan, HospitalTemplate


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
