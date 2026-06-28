from django.contrib import admin
from .models import DeveloperProfile, Skill, DeveloperSkill, Certification, PortfolioProject, Subscription

admin.site.register(Skill)
admin.site.register(DeveloperSkill)
admin.site.register(Certification)
admin.site.register(PortfolioProject)
admin.site.register(Subscription)

@admin.register(DeveloperProfile)
class DeveloperProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'availability', 'hourly_rate', 'experience_years']
    search_fields = ['user__email', 'bio']
