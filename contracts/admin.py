from django.contrib import admin
from .models import Contract, Milestone, Deliverable

admin.site.register(Deliverable)

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['project', 'total_amount', 'status', 'start_date']
    list_filter = ['status']

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'contract', 'amount', 'status', 'due_date']
    list_filter = ['status']
