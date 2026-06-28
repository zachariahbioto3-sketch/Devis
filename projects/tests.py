import uuid

from django.test import TestCase
from django.urls import reverse


class ProjectViewsTests(TestCase):
    def test_browse_projects_renders_template(self):
        response = self.client.get(reverse("browse_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/browse.html")

    def test_project_detail_renders_template(self):
        response = self.client.get(reverse("project_detail", args=[uuid.uuid4()]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects/detail.html")
