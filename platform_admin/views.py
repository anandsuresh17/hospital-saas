
from django.shortcuts import render


# Dashboard
def dashboard(request):
    return render(request, "dashboard.html")


# Hospital Management
def hospital_list(request):
    return render(request, "hospital_list.html")


def hospital_create(request):
    return render(request, "hospital_form.html", {
        "page_title": "Add Hospital",
        "button_text": "Create Hospital",
    })


def hospital_update(request, pk):
    return render(request, "hospital_form.html", {
        "page_title": "Edit Hospital",
        "button_text": "Save Changes",
        "record_id": pk,
    })


def hospital_delete(request, pk):
    return render(request, "hospital_confirm_delete.html", {
        "page_title": "Delete Hospital",
        "record_id": pk,
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
