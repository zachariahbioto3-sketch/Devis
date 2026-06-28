from django import forms
from .models import Project
from developers.models import Skill

INPUT = "w-full bg-dark-700 border border-dark-600 rounded-lg px-4 py-2.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-brand-500 transition-colors"
SELECT = "w-full bg-dark-700 border border-dark-600 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-brand-500 transition-colors"
TEXTAREA = "w-full bg-dark-700 border border-dark-600 rounded-lg px-4 py-2.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-brand-500 transition-colors resize-none"

class ProjectForm(forms.ModelForm):
    skills_required = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Project
        fields = [
            "title", "description", "category",
            "budget_min", "budget_max", "deadline",
            "skills_required", "is_remote",
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": INPUT,
                "placeholder": "e.g. Build a Django e-commerce site with M-Pesa",
            }),
            "description": forms.Textarea(attrs={
                "class": TEXTAREA,
                "rows": 6,
                "placeholder": "Describe your project in detail. Include what you need built, any existing systems to integrate with, and preferred tech stack.",
            }),
            "category": forms.Select(attrs={"class": SELECT}),
            "budget_min": forms.NumberInput(attrs={
                "class": INPUT, "placeholder": "e.g. 15000",
            }),
            "budget_max": forms.NumberInput(attrs={
                "class": INPUT, "placeholder": "e.g. 50000",
            }),
            "deadline": forms.DateInput(attrs={
                "class": INPUT, "type": "date",
            }),
            "is_remote": forms.CheckboxInput(attrs={
                "class": "w-4 h-4 rounded border-dark-500 bg-dark-700 text-brand-500 focus:ring-brand-500",
            }),
        }

    def clean(self):
        cleaned = super().clean()
        bmin = cleaned.get("budget_min")
        bmax = cleaned.get("budget_max")
        if bmin and bmax and bmax < bmin:
            raise forms.ValidationError("Maximum budget cannot be less than minimum budget.")
        return cleaned
