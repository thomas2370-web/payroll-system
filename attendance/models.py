from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import User
from staff.models import Teacher


class AttendanceRecord(models.Model):
    """
    One row per teacher per school day. Populated by two QR scans
    (check-in, check-out) performed by the Discipline Master.
    """
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="attendance_records")
    session_date = models.DateField()
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    scanned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="scans")

    class Meta:
        unique_together = ("teacher", "session_date")
        ordering = ["-session_date"]

    @property
    def hours_worked(self) -> Decimal:
        if not (self.check_in and self.check_out):
            return Decimal("0.00")
        seconds = (self.check_out - self.check_in).total_seconds()
        return round(Decimal(seconds) / Decimal(3600), 2)

    def __str__(self):
        return f"{self.teacher.name} - {self.session_date}"


class Adjustment(models.Model):
    """
    A disciplinary hour deduction (late arrival, abandoned lecture, etc.).
    `justification` is mandatory at the database level — this is what
    guarantees the audit trail described in the report's problem statement.
    """
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="adjustments")
    attendance_record = models.ForeignKey(
        AttendanceRecord, on_delete=models.CASCADE, related_name="adjustments"
    )
    deduct_hours = models.DecimalField(max_digits=5, decimal_places=2)
    justification = models.TextField()
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.justification or not self.justification.strip():
            raise ValidationError("A written justification is required before a penalty can be saved.")
        if self.deduct_hours <= 0:
            raise ValidationError("Deducted hours must be a positive amount.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"-{self.deduct_hours}h for {self.teacher.name} on {self.attendance_record.session_date}"
