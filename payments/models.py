import uuid
from django.db import models


class Payment(models.Model):
    METHOD_MPESA = 'mpesa'
    METHOD_STRIPE = 'stripe'
    METHOD_CHOICES = [
        (METHOD_MPESA, 'M-Pesa'),
        (METHOD_STRIPE, 'Stripe'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    TYPE_CHOICES = [
        ('milestone', 'Milestone Payment'),
        ('product', 'Product Purchase'),
        ('subscription', 'Subscription'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    milestone = models.OneToOneField('contracts.Milestone', on_delete=models.SET_NULL, null=True, blank=True, related_name='payment')
    product_purchase = models.OneToOneField('store.ProductPurchase', on_delete=models.SET_NULL, null=True, blank=True, related_name='payment')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    mpesa_ref = models.CharField(max_length=100, blank=True)
    mpesa_receipt = models.CharField(max_length=100, blank=True)
    stripe_payment_intent = models.CharField(max_length=200, blank=True)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.payment_type} — KES {self.amount} [{self.status}]'

    @property
    def developer_payout(self):
        return self.amount - self.platform_fee
