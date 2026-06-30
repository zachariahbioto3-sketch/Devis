from django import forms
from .models import SoftwareProduct

INPUT = "w-full bg-dark-700 border border-dark-600 rounded-lg px-4 py-2.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-brand-500 transition-colors"
SELECT = "w-full bg-dark-700 border border-dark-600 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-brand-500 transition-colors"
TEXTAREA = "w-full bg-dark-700 border border-dark-600 rounded-lg px-4 py-2.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-brand-500 transition-colors resize-none"


class SoftwareProductForm(forms.ModelForm):
    class Meta:
        model = SoftwareProduct
        fields = [
            "title", "short_description", "description", "category",
            "price", "tech_stack", "thumbnail", "demo_url", "repo_url",
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": INPUT, "placeholder": "e.g. Django E-commerce Starter Kit",
            }),
            "short_description": forms.TextInput(attrs={
                "class": INPUT, "placeholder": "One-line pitch, shown in listings", "maxlength": 300,
            }),
            "description": forms.Textarea(attrs={
                "class": TEXTAREA, "rows": 6,
                "placeholder": "Full description: features, what is included, who it is for, setup requirements.",
            }),
            "category": forms.Select(attrs={"class": SELECT}),
            "price": forms.NumberInput(attrs={
                "class": INPUT, "placeholder": "e.g. 8000",
            }),
            "tech_stack": forms.TextInput(attrs={
                "class": INPUT, "placeholder": "Django, PostgreSQL, Tailwind, M-Pesa (comma separated)",
            }),
            "demo_url": forms.URLInput(attrs={
                "class": INPUT, "placeholder": "https://your-demo-site.com",
            }),
            "repo_url": forms.URLInput(attrs={
                "class": INPUT, "placeholder": "Private repo link — only shown to buyers after purchase",
            }),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        from django.utils.text import slugify
        self.slug = slugify(title)
        return title
