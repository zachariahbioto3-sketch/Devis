from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DeveloperViewsTests(TestCase):
    def test_dashboard_renders_template_for_authenticated_user(self):
        user = get_user_model().objects.create_user(username="dev", email="dev@example.com", password="secret123")
        self.client.force_login(user)

        response = self.client.get(reverse("dev_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "developers/dashboard.html")

    def test_public_profile_renders_template(self):
        response = self.client.get(reverse("dev_public_profile", args=["alex"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "developers/public_profile.html")
