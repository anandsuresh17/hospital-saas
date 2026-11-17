
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.utils import timezone

from .models import (
    Hospital,
    SubscriptionPlan,
    HospitalTemplate,
    SubscriptionRequest,
)

from .forms import (
    HospitalForm,
    SubscriptionPlanForm,
    HospitalTemplateForm,
)


# ==========================================
# SUPER ADMIN ACCESS
# ==========================================

def is_super_admin(user):
    return user.is_authenticated and user.is_superuser


# ==========================================
# SUPER ADMIN DASHBOARD
# ==========================================

def dashboard(request):
    return render(request, "dashboard.html")


# ==========================================
# HOSPITAL MANAGEMENT
# ==========================================

def hospital_list(request):
    hospitals = Hospital.objects.all()

    return render(request, "hospital_list.html", {
        "hospitals": hospitals,
    })


def hospital_create(request):
    if request.method == "POST":
        form = HospitalForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("hospital_list")
    else:
        form = HospitalForm()

    return render(request, "hospital_form.html", {
        "form": form,
        "page_title": "Add Hospital",
        "button_text": "Create Hospital",
    })


def hospital_update(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)

    if request.method == "POST":
        form = HospitalForm(request.POST, instance=hospital)

        if form.is_valid():
            form.save()
            return redirect("hospital_list")
    else:
        form = HospitalForm(instance=hospital)

    return render(request, "hospital_form.html", {
        "form": form,
        "page_title": "Edit Hospital",
        "button_text": "Save Changes",
    })


def hospital_delete(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)

    if request.method == "POST":
        hospital.is_active = False
        hospital.save()
        return redirect("hospital_list")

    return render(request, "hospital_confirm_delete.html", {
        "hospital": hospital,
        "page_title": "Deactivate Hospital",
    })


def hospital_activate(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)

    if request.method == "POST":
        hospital.is_active = True
        hospital.save()
        return redirect("hospital_list")

    return render(request, "hospital_activate.html", {
        "hospital": hospital,
        "page_title": "Activate Hospital",
    })


# ==========================================
# SUBSCRIPTION PLAN MANAGEMENT
# ==========================================

def subscription_list(request):
    plans = SubscriptionPlan.objects.all()

    return render(request, "subscription_list.html", {
        "plans": plans,
    })


def subscription_create(request):
    if request.method == "POST":
        form = SubscriptionPlanForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("subscription_list")
    else:
        form = SubscriptionPlanForm()

    return render(request, "subscription_form.html", {
        "form": form,
        "page_title": "Add Subscription Plan",
        "button_text": "Create Plan",
    })


def subscription_update(request, pk):
    plan = get_object_or_404(SubscriptionPlan, pk=pk)

    if request.method == "POST":
        form = SubscriptionPlanForm(request.POST, instance=plan)

        if form.is_valid():
            form.save()
            return redirect("subscription_list")
    else:
        form = SubscriptionPlanForm(instance=plan)

    return render(request, "subscription_form.html", {
        "form": form,
        "page_title": "Edit Subscription Plan",
        "button_text": "Save Changes",
    })


def subscription_delete(request, pk):
    plan = get_object_or_404(SubscriptionPlan, pk=pk)

    if request.method == "POST":
        plan.is_active = False
        plan.save()
        return redirect("subscription_list")

    return render(request, "subscription_confirm_delete.html", {
        "plan": plan,
        "page_title": "Deactivate Subscription Plan",
    })


def subscription_activate(request, pk):
    plan = get_object_or_404(SubscriptionPlan, pk=pk)

    if request.method == "POST":
        plan.is_active = True
        plan.save()
        return redirect("subscription_list")

    return render(request, "subscription_activate.html", {
        "plan": plan,
        "page_title": "Activate Subscription Plan",
    })


# ==========================================
# HOSPITAL TEMPLATE MANAGEMENT
# ==========================================

def template_list(request):
    templates = HospitalTemplate.objects.all()

    return render(request, "template_list.html", {
        "templates": templates
    })


def template_create(request):
    if request.method == "POST":
        form = HospitalTemplateForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("template_list")
    else:
        form = HospitalTemplateForm()

    return render(request, "template_form.html", {
        "form": form,
        "page_title": "Add Hospital Template",
        "button_text": "Create Template",
    })


def template_update(request, pk):
    template = get_object_or_404(HospitalTemplate, pk=pk)

    if request.method == "POST":
        form = HospitalTemplateForm(
            request.POST,
            request.FILES,
            instance=template
        )

        if form.is_valid():
            form.save()
            return redirect("template_list")
    else:
        form = HospitalTemplateForm(instance=template)

    return render(request, "template_form.html", {
        "form": form,
        "page_title": "Edit Hospital Template",
        "button_text": "Save Changes",
    })


def template_delete(request, pk):
    template = get_object_or_404(HospitalTemplate, pk=pk)

    if request.method == "POST":
        template.is_active = False
        template.save()
        return redirect("template_list")

    return render(request, "template_confirm_delete.html", {
        "template": template,
        "page_title": "Deactivate Hospital Template",
    })


def template_activate(request, pk):
    template = get_object_or_404(HospitalTemplate, pk=pk)

    if request.method == "POST":
        template.is_active = True
        template.save()
        return redirect("template_list")

    return render(request, "template_activate.html", {
        "template": template,
        "page_title": "Activate Hospital Template",
    })


# ==========================================
# SUBSCRIPTION REQUEST MANAGEMENT
# ==========================================

@login_required
@user_passes_test(is_super_admin)
def subscription_requests(request):

    requests = SubscriptionRequest.objects.select_related(
        'hospital',
        'current_plan',
        'requested_plan'
    ).order_by('-created_at')

    return render(
        request,
        "subscription_requests.html",
        {
            "requests": requests,
        }
    )


@login_required
@user_passes_test(is_super_admin)
def review_subscription_request(request, pk):

    subscription_request = get_object_or_404(
        SubscriptionRequest.objects.select_related(
            'hospital',
            'current_plan',
            'requested_plan'
        ),
        pk=pk
    )

    if request.method == "POST":

        action = request.POST.get("action")
        remarks = request.POST.get("admin_remarks", "").strip()

        if action not in ["approve", "reject"]:
            messages.error(request, "Invalid action.")
            return redirect(
                "review_subscription_request",
                pk=pk
            )

        with transaction.atomic():

            subscription_request = get_object_or_404(
                SubscriptionRequest.objects.select_for_update(),
                pk=pk
            )

            if subscription_request.status != "Pending":
                messages.warning(
                    request,
                    "This request has already been reviewed."
                )
                return redirect("subscription_requests")

            if action == "approve":

                hospital = get_object_or_404(
                    Hospital.objects.select_for_update(),
                    pk=subscription_request.hospital_id
                )

                today = timezone.localdate()

                # If the current subscription is still active,
                # the new subscription begins after its expiry.
                start_date = today

                if (
                    hospital.subscription_end_date
                    and hospital.subscription_end_date >= today
                ):
                    start_date = (
                        hospital.subscription_end_date
                        + timedelta(days=1)
                    )

                hospital.subscription_plan = (
                    subscription_request.requested_plan
                )

                hospital.subscription_start_date = start_date

                hospital.subscription_end_date = (
                    start_date
                    + timedelta(
                        days=subscription_request.requested_plan.duration_days - 1
                    )
                )

                hospital.save(update_fields=[
                    "subscription_plan",
                    "subscription_start_date",
                    "subscription_end_date",
                    "updated_at",
                ])

                subscription_request.status = "Approved"

                messages.success(
                    request,
                    "Subscription request approved successfully."
                )

            else:

                subscription_request.status = "Rejected"

                messages.success(
                    request,
                    "Subscription request rejected."
                )

            subscription_request.admin_remarks = remarks
            subscription_request.reviewed_at = timezone.now()

            subscription_request.save(update_fields=[
                "status",
                "admin_remarks",
                "reviewed_at",
            ])

        return redirect("subscription_requests")

    return render(
        request,
        "review_subscription_request.html",
        {
            "subscription_request": subscription_request,
        }
    )
