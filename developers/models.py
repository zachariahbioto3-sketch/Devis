import uuid
from django.db import models
from django.conf import settings


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class DeveloperProfile(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('unavailable', 'Unavailable'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dev_profile')
    bio = models.TextField(blank=True)
    tagline = models.CharField(max_length=200, blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    skills = models.ManyToManyField(Skill, through='DeveloperSkill', blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')
    location = models.CharField(max_length=100, default='Kenya')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.email


class DeveloperSkill(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]
    developer = models.ForeignKey(DeveloperProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='intermediate')

    class Meta:
        unique_together = ('developer', 'skill')


class Certification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    developer = models.ForeignKey(DeveloperProfile, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    issued_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True)

    def __str__(self):
        return f'{self.title} — {self.issuer}'


class PortfolioProject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    developer = models.ForeignKey(DeveloperProfile, on_delete=models.CASCADE, related_name='portfolio_projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=300, blank=True, help_text='Comma separated, e.g. Django,React,PostgreSQL')
    thumbnail = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    live_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    PLAN_FREE = 'free'
    PLAN_PRO = 'pro'
    PLAN_CHOICES = [
        (PLAN_FREE, 'Free'),
        (PLAN_PRO, 'Pro — KES 999/mo'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    developer = models.OneToOneField(DeveloperProfile, on_delete=models.CASCADE, related_name='subscription')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default=PLAN_FREE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mpesa_ref = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.developer} — {self.plan}'
