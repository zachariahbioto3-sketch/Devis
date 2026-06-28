from django.urls import path
from . import views

urlpatterns = [
    path("mpesa/initiate/", views.mpesa_initiate, name="mpesa_initiate"),
    path("mpesa/callback/", views.mpesa_callback, name="mpesa_callback"),
    path("milestone/<uuid:milestone_pk>/pay/", views.pay_milestone, name="pay_milestone"),
    path("subscription/pay/", views.pay_subscription, name="pay_subscription"),
]
