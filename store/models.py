import uuid
from django.db import models
from django.conf import settings


class SoftwareProduct(models.Model):
    CATEGORY_CHOICES = [
        ('template', 'Website Template'),
        ('saas', 'SaaS Starter'),
        ('plugin', 'Plugin / Extension'),
        ('script', 'Script / Tool'),
        ('mobile', 'Mobile App'),
        ('api', 'API / Service'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    developer = models.ForeignKey('developers.DeveloperProfile', on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    tech_stack = models.CharField(max_length=300, blank=True)
    thumbnail = models.ImageField(upload_to='products/', blank=True, null=True)
    demo_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True, help_text='Private until purchased')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_tech_list(self):
        if not self.tech_stack:
            return []
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()][:5]


class ProductPurchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(SoftwareProduct, on_delete=models.CASCADE, related_name='purchases')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchases')
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    mpesa_ref = models.CharField(max_length=100, blank=True)
    stripe_ref = models.CharField(max_length=100, blank=True)
    purchased_at = models.DateTimeField(auto_now_add=True)
    download_token = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.buyer.email} bought {self.product.title}'
