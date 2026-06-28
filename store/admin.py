from django.contrib import admin
from .models import SoftwareProduct, ProductPurchase

@admin.register(SoftwareProduct)
class SoftwareProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'developer', 'category', 'price', 'is_active']
    list_filter = ['category', 'is_active']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ProductPurchase)
class ProductPurchaseAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'product', 'amount_paid', 'purchased_at']
