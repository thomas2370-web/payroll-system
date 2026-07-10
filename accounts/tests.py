from django.contrib.auth import get_user_model
from django.core.management import call_command
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

    def test_super_admin_role_is_detected(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="super_admin_demo",
            password="secret123",
            role=User.Role.SUPER_ADMIN,
        )

        self.assertTrue(user.is_super_admin)

    def test_seed_demo_data_creates_role_accounts_with_thegame(self):
        call_command("seed_demo_data")

        User = get_user_model()
        for username, role in [
            ("super_admin", "SUPER_ADMIN"),
            ("principal", "PRINCIPAL"),
            ("discipline", "DISCIPLINE_MASTER"),
            ("accountant", "ACCOUNTANT"),
            ("proprietor", "PROPRIETOR"),
            ("teacher_demo", "TEACHER"),
        ]:
            user = User.objects.get(username=username)
            self.assertEqual(user.role, role)
            self.assertTrue(user.check_password("thegame"))
