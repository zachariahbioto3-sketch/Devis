from django.test import TestCase
from django.urls import reverse


class StoreViewsTests(TestCase):
    def test_marketplace_renders_template(self):
        response = self.client.get(reverse("marketplace"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "store/marketplace.html")
