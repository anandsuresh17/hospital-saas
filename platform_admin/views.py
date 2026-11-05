
from django.shortcuts import render, redirect, get_object_or_404

from .models import Hospital
from .forms import HospitalForm


# Dashboard
def dashboard(request):
    return render(request, "dashboard.html")


# Hospital Management
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


# Deactivate Hospital
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


# Activate Hospital
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


# Subscription Plans
def subscription_list(request):
    return render(request, "subscription_list.html")


def subscription_create(request):
    return render(request, "subscription_form.html", {
        "page_title": "Add Subscription Plan",
        "button_text": "Create Plan",
    })


def subscription_update(request, pk):
    return render(request, "subscription_form.html", {
        "page_title": "Edit Subscription Plan",
        "button_text": "Save Changes",
        "record_id": pk,
    })


def subscription_delete(request, pk):
    return render(request, "hospital_confirm_delete.html", {
        "page_title": "Delete Subscription Plan",
        "record_id": pk,
    })


# Hospital Templates
def template_list(request):
    return render(request, "template_list.html")


def template_create(request):
    return render(request, "template_form.html", {
        "page_title": "Add Hospital Template",
        "button_text": "Create Template",
    })


def template_update(request, pk):
    return render(request, "template_form.html", {
        "page_title": "Edit Hospital Template",
        "button_text": "Save Changes",
        "record_id": pk,
    })


def template_delete(request, pk):
    return render(request, "hospital_confirm_delete.html", {
        "page_title": "Delete Hospital Template",
        "record_id": pk,
    })
