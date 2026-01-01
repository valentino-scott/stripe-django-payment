"""
URL configuration for stripe_demo_project project.
"""

from django.contrib import admin
from django.urls import path
from payments import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path('history/', views.payment_history, name='payment_history'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]