from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from staff.models import Teacher

User = get_user_model()

DEMO_USERS = [
    ("principal", "PRINCIPAL", "Amina Njoya"),
    ("discipline", "DISCIPLINE_MASTER", "Paul Etoundi"),
    ("accountant", "ACCOUNTANT", "Brenda Fon"),
    ("proprietor", "PROPRIETOR", "Dr. Jean Kamga"),
]
DEMO_PASSWORD = "changeme123"


class Command(BaseCommand):
    help = "Creates one demo login per role (password: changeme123) plus a sample teacher, for evaluation only."

    @transaction.atomic
    def handle(self, *args, **options):
        for username, role, full_name in DEMO_USERS:
            first, _, last = full_name.partition(" ")
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"role": role, "first_name": first, "last_name": last},
            )
            if created:
                user.set_password(DEMO_PASSWORD)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created {role} login: {username} / {DEMO_PASSWORD}"))
            else:
                self.stdout.write(f"{username} already exists, skipped.")

        teacher_user, created = User.objects.get_or_create(
            username="teacher_demo",
            defaults={"role": "TEACHER", "first_name": "Grace", "last_name": "Manga"},
        )
        if created:
            teacher_user.set_password(DEMO_PASSWORD)
            teacher_user.save()

        if not Teacher.objects.filter(user=teacher_user).exists():
            Teacher.objects.create(
                user=teacher_user,
                name="Grace Manga",
                subject="Mathematics",
                hourly_rate=2500,
                expected_weekly_hours=20,
            )
            self.stdout.write(self.style.SUCCESS("Created demo teacher: teacher_demo / changeme123"))

        self.stdout.write(self.style.SUCCESS(
            "\nDemo logins ready (all passwords: changeme123):\n"
            "  principal / discipline / accountant / proprietor / teacher_demo\n"
            "Also run 'python manage.py createsuperuser' for full admin access."
        ))
