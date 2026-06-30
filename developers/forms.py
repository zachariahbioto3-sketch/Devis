from django import forms
from .models import DeveloperProfile, Certification, PortfolioProject, DeveloperSkill, Skill

INPUT = "w-full bg-dark-700 border border-dark-600 rounded-lg px-4 py-2.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-brand-500 transition-colors"
SELECT = "w-full bg-dark-700 border border-dark-600 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-brand-500 transition-colors"
TEXTAREA = "w-full bg-dark-700 border border-dark-600 rounded-lg px-4 py-2.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-brand-500 transition-colors resize-none"


class DeveloperProfileForm(forms.ModelForm):
    class Meta:
        model = DeveloperProfile
        fields = [
            "tagline", "bio", "hourly_rate", "experience_years",
            "github_url", "portfolio_url", "availability", "location",
        ]
        widgets = {
            "tagline": forms.TextInput(attrs={
                "class": INPUT, "placeholder": "e.g. Django developer specializing in fintech & M-Pesa integrations",
            }),
            "bio": forms.Textarea(attrs={
                "class": TEXTAREA, "rows": 5,
                "placeholder": "Tell clients about your experience, what you specialize in, and how you work.",
            }),
            "hourly_rate": forms.NumberInput(attrs={
                "class": INPUT, "placeholder": "e.g. 1500",
            }),
            "experience_years": forms.NumberInput(attrs={
                "class": INPUT, "placeholder": "e.g. 3",
            }),
            "github_url": forms.URLInput(attrs={
                "class": INPUT, "placeholder": "https://github.com/yourusername",
            }),
            "portfolio_url": forms.URLInput(attrs={
                "class": INPUT, "placeholder": "https://yourportfolio.com",
            }),
            "availability": forms.Select(attrs={"class": SELECT}),
            "location": forms.TextInput(attrs={
                "class": INPUT, "placeholder": "e.g. Kaimosi, Kenya",
            }),
        }


class PortfolioProjectForm(forms.ModelForm):
    class Meta:
        model = PortfolioProject
        fields = ["title", "description", "tech_stack", "thumbnail", "live_url", "repo_url"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": INPUT, "placeholder": "e.g. BookBase — Digital Bookstore Platform",
            }),
            "description": forms.Textarea(attrs={
                "class": TEXTAREA, "rows": 4,
                "placeholder": "What did you build? What problem did it solve?",
            }),
            "tech_stack": forms.TextInput(attrs={
                "class": INPUT, "placeholder": "Django, PostgreSQL, M-Pesa (comma separated)",
            }),
            "live_url": forms.URLInput(attrs={"class": INPUT, "placeholder": "https://liveproject.com"}),
            "repo_url": forms.URLInput(attrs={"class": INPUT, "placeholder": "https://github.com/you/project"}),
        }


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ["title", "issuer", "issued_date", "expiry_date", "credential_url"]
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT, "placeholder": "e.g. AWS Certified Developer"}),
            "issuer": forms.TextInput(attrs={"class": INPUT, "placeholder": "e.g. Amazon Web Services"}),
            "issued_date": forms.DateInput(attrs={"class": INPUT, "type": "date"}),
            "expiry_date": forms.DateInput(attrs={"class": INPUT, "type": "date"}),
            "credential_url": forms.URLInput(attrs={"class": INPUT, "placeholder": "Verification link"}),
        }
