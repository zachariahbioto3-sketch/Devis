from django.contrib import admin
from .models import Project, Bid

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'category', 'status', 'budget_min', 'budget_max', 'created_at']
    list_filter = ['status', 'category']
    search_fields = ['title', 'description']

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['developer', 'project', 'amount', 'timeline_days', 'status']
    list_filter = ['status']
