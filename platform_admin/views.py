
from django.shortcuts import render, redirect, get_object_or_404

from .models import Hospital, SubscriptionPlan, HospitalTemplate
from .forms import HospitalForm, SubscriptionPlanForm, HospitalTemplateForm


# ==============================
# SUPER ADMIN DASHBOARD
# ==============================

def dashboard(request):
    return render(request, "dashboard.html")


# ==============================
# HOSPITAL MANAGEMENT
# ==============================

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


# ==============================
# SUBSCRIPTION PLAN MANAGEMENT
# ==============================

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


# ==============================
# HOSPITAL TEMPLATE MANAGEMENT
# ==============================

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
