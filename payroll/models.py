from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from accounts.models import User
from staff.models import FixedStaff, Teacher


class PaymentSheet(models.Model):
    """
    One payment sheet per calendar month. Moves through a strict
    status chain enforced by payroll.services, mirroring the
    Approval Workflow in Chapter 2/3 of the report:

        DRAFT -> PENDING_APPROVAL -> APPROVED -> DISBURSED
                                   -> REJECTED (back to DRAFT)
    """

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PENDING_APPROVAL = "PENDING_APPROVAL", "Pending approval"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        DISBURSED = "DISBURSED", "Disbursed"

    month = models.DateField(help_text="Use the first day of the target month, e.g. 2026-07-01")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    submitted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="sheets_submitted"
    )
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sheets_approved"
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    class Meta:
        unique_together = ("month",)
        ordering = ["-month"]

    def __str__(self):
        return f"Payment sheet {self.month:%B %Y} ({self.get_status_display()})"


class SalaryEntry(models.Model):
    """
    One line item per staff member on a payment sheet. Exactly one of
    `teacher` / `fixed_staff` must be set, unifying the two salary
    models described in the report (hourly vs fixed).
    """
    sheet = models.ForeignKey(PaymentSheet, on_delete=models.CASCADE, related_name="entries")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    fixed_staff = models.ForeignKey(FixedStaff, on_delete=models.SET_NULL, null=True, blank=True)

    adjusted_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    signed = models.BooleanField(default=False)
    signed_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if bool(self.teacher) == bool(self.fixed_staff):
            raise ValidationError("A salary entry must reference exactly one of teacher or fixed_staff.")

    def mark_signed(self):
        self.signed = True
        self.signed_at = timezone.now()
        self.save(update_fields=["signed", "signed_at"])

    @property
    def staff_name(self):
        return self.teacher.name if self.teacher else self.fixed_staff.name

    def __str__(self):
        return f"{self.staff_name} — {self.amount} CFA"
