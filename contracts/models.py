import uuid
from django.db import models


class Contract(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('disputed', 'Disputed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.OneToOneField('projects.Project', on_delete=models.CASCADE, related_name='contract')
    bid = models.OneToOneField('projects.Bid', on_delete=models.SET_NULL, null=True, related_name='contract')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    terms = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Contract: {self.project.title}'


class Milestone(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted for Review'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.contract.project.title} — {self.title}'


class Deliverable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, related_name='deliverables')
    file = models.FileField(upload_to='deliverables/', blank=True, null=True)
    file_url = models.URLField(blank=True, help_text='External link e.g. GitHub, Google Drive')
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f'Deliverable for {self.milestone.title}'
