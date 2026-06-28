import uuid
from django.db import models
from django.conf import settings
from developers.models import Skill


class Project(models.Model):
    STATUS_OPEN = 'open'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    CATEGORY_CHOICES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile App'),
        ('api', 'API / Backend'),
        ('data', 'Data & Analytics'),
        ('design', 'UI/UX Design'),
        ('ecommerce', 'E-commerce'),
        ('automation', 'Automation'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey('clients.ClientProfile', on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=300)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    skills_required = models.ManyToManyField(Skill, blank=True)
    budget_min = models.DecimalField(max_digits=12, decimal_places=2)
    budget_max = models.DecimalField(max_digits=12, decimal_places=2)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    is_remote = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Bid(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='bids')
    developer = models.ForeignKey('developers.DeveloperProfile', on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timeline_days = models.PositiveIntegerField()
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'developer')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.developer} → {self.project}'
