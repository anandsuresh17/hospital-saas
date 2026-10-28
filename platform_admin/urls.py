
from django.urls import path
from . import views

urlpatterns = [
    # Super Admin Dashboard
    path('', views.dashboard, name='platform_dashboard'),

    # Hospital Management
    path('hospitals/', views.hospital_list, name='hospital_list'),
    path('hospitals/add/', views.hospital_create, name='hospital_create'),
    path('hospitals/<int:pk>/edit/', views.hospital_update, name='hospital_update'),
    path('hospitals/<int:pk>/delete/', views.hospital_delete, name='hospital_delete'),

    # Subscription Plan Management
    path('subscriptions/', views.subscription_list, name='subscription_list'),
    path('subscriptions/add/', views.subscription_create, name='subscription_create'),
    path('subscriptions/<int:pk>/edit/', views.subscription_update, name='subscription_update'),
    path('subscriptions/<int:pk>/delete/', views.subscription_delete, name='subscription_delete'),

    # Hospital Template Management
    path('templates/', views.template_list, name='template_list'),
    path('templates/add/', views.template_create, name='template_create'),
    path('templates/<int:pk>/edit/', views.template_update, name='template_update'),
    path('templates/<int:pk>/delete/', views.template_delete, name='template_delete'),
]
