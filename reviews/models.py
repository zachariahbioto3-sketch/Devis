import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    REVIEW_FOR_CHOICES = [
        ('developer', 'Developer'),
        ('client', 'Client'),
        ('product', 'Software Product'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    reviewee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews_received')
    product = models.ForeignKey('store.SoftwareProduct', on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    contract = models.ForeignKey('contracts.Contract', on_delete=models.SET_NULL, null=True, blank=True)
    review_for = models.CharField(max_length=20, choices=REVIEW_FOR_CHOICES)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.reviewer.email} → {self.rating}★'
