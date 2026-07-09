from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DashboardViewTests(TestCase):
    def test_authenticated_user_can_access_dashboard(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="accountant_demo",
            email="accountant@example.com",
            password="secret123",
            role=User.Role.ACCOUNTANT,
        )

        self.client.force_login(user)
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Payroll Control Center")
