import os

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        if os.environ.get("RUN_MAIN") != "true":
            return
        from django.conf import settings

        if settings.DEBUG:
            return

        from django.core.management import call_command

        call_command("seed_demo_data", verbosity=0)
