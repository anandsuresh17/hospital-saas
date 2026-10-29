
from django.urls import path
from . import views

urlpatterns = [
    path('<slug:hospital_slug>/', views.home, name='hospital_site_home'),
    path('<slug:hospital_slug>/about/', views.about, name='hospital_site_about'),
    path('<slug:hospital_slug>/departments/', views.departments, name='hospital_site_departments'),
    path('<slug:hospital_slug>/doctors/', views.doctors, name='hospital_site_doctors'),
    path('<slug:hospital_slug>/appointment/', views.appointment_form, name='hospital_site_appointment'),
    path('<slug:hospital_slug>/contact/', views.contact, name='hospital_site_contact'),
]
