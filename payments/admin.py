from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_type', 'amount', 'method', 'status', 'created_at']
    list_filter = ['status', 'method', 'payment_type']
    search_fields = ['mpesa_ref', 'stripe_payment_intent']
