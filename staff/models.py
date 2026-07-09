import io
import uuid

import qrcode
from django.core.files.base import ContentFile
from django.db import models

from accounts.models import User


class Teacher(models.Model):
    """
    An hourly-rate staff member. Registered by the Principal.
    Salary = Adjusted Hours x Hourly Rate (see payroll.services).
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="teacher_profile",
        null=True, blank=True,
    )
    name = models.CharField(max_length=150)
    subject = models.CharField(max_length=100)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    expected_weekly_hours = models.PositiveIntegerField()

    # A stable, unguessable identifier encoded into the QR code.
    # Using a UUID (rather than the DB primary key) means the code can't
    # be trivially enumerated or guessed from a low staff id.
    qr_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    qr_image = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new or not self.qr_image:
            self._generate_qr_code()

    def _generate_qr_code(self):
        """Encode the teacher's qr_token into a QR image and attach it."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # 30% damage-tolerant
            box_size=10,
            border=4,
        )
        qr.add_data(str(self.qr_token))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        filename = f"teacher_{self.pk}_{self.qr_token.hex[:8]}.png"
        self.qr_image.save(filename, ContentFile(buffer.getvalue()), save=False)
        super().save(update_fields=["qr_image"])

    def __str__(self):
        return f"{self.name} ({self.subject})"


class FixedStaff(models.Model):
    """
    Salaried staff (Principal, Accountant, admin assistants) who receive
    a predetermined monthly amount regardless of hours worked.
    Added by the Accountant at month end.
    """
    name = models.CharField(max_length=150)
    role_title = models.CharField(max_length=100)
    fixed_salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.role_title})"
