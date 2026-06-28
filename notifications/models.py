import uuid
from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_CHOICES = [
        ('bid_received', 'New bid on your project'),
        ('bid_accepted', 'Your bid was accepted'),
        ('bid_rejected', 'Your bid was rejected'),
        ('milestone_submitted', 'Deliverable submitted'),
        ('milestone_approved', 'Milestone approved'),
        ('payment_released', 'Payment released'),
        ('message', 'New message'),
        ('review', 'New review'),
        ('subscription', 'Subscription update'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    message = models.TextField()
    link = models.CharField(max_length=300, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} — {self.notification_type}'
