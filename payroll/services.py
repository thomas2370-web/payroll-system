"""
Core payroll logic: salary computation, sheet submission, approval,
rejection and disbursement. Keeping this out of views/models means the
same functions can be called from the web UI, the admin, or a test suite.
"""
from __future__ import annotations

from decimal import Decimal

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone

from attendance.models import AttendanceRecord
from payroll.models import PaymentSheet, SalaryEntry
from staff.models import FixedStaff, Teacher


def compute_teacher_salary(teacher: Teacher, month_start, month_end) -> tuple[Decimal, Decimal]:
    """
    Adjusted Hours = sum(recorded hours) - sum(penalty deductions)
    Salary = Adjusted Hours x Hourly Rate
    Returns (adjusted_hours, salary_amount).
    """
    records = AttendanceRecord.objects.filter(
        teacher=teacher, session_date__gte=month_start, session_date__lte=month_end
    )

    total_hours = sum((r.hours_worked for r in records), Decimal("0.00"))
    total_deductions = sum(
        (a.deduct_hours for r in records for a in r.adjustments.all()), Decimal("0.00")
    )

    adjusted_hours = max(total_hours - total_deductions, Decimal("0.00"))
    salary = (adjusted_hours * teacher.hourly_rate).quantize(Decimal("0.01"))
    return adjusted_hours, salary


@transaction.atomic
def generate_payment_sheet(month_start, month_end, submitted_by):
    """
    Called by the Accountant at month end. Computes salaries for every
    active teacher and rolls in active fixed-salary staff, producing a
    DRAFT payment sheet ready for review before submission.
    """
    sheet, created = PaymentSheet.objects.get_or_create(
        month=month_start, defaults={"submitted_by": submitted_by}
    )
    if sheet.status != PaymentSheet.Status.DRAFT:
        raise ValidationError("Only a DRAFT sheet can be (re)generated.")

    sheet.entries.all().delete()

    for teacher in Teacher.objects.filter(is_active=True):
        adjusted_hours, amount = compute_teacher_salary(teacher, month_start, month_end)
        SalaryEntry.objects.create(
            sheet=sheet, teacher=teacher, adjusted_hours=adjusted_hours, amount=amount
        )

    for staff_member in FixedStaff.objects.filter(is_active=True):
        SalaryEntry.objects.create(
            sheet=sheet, fixed_staff=staff_member, amount=staff_member.fixed_salary
        )

    return sheet


def submit_for_approval(sheet: PaymentSheet, submitted_by):
    if sheet.status != PaymentSheet.Status.DRAFT:
        raise ValidationError("Only a DRAFT sheet can be submitted for approval.")
    if not submitted_by.is_accountant:
        raise PermissionDenied("Only the Accountant can submit a payment sheet.")

    sheet.status = PaymentSheet.Status.PENDING_APPROVAL
    sheet.submitted_by = submitted_by
    sheet.save(update_fields=["status", "submitted_by"])
    return sheet


def approve_sheet(sheet: PaymentSheet, approved_by):
    if not approved_by.is_proprietor:
        raise PermissionDenied("Only the Proprietor can approve a payment sheet.")
    if sheet.status != PaymentSheet.Status.PENDING_APPROVAL:
        raise ValidationError("Only a sheet pending approval can be approved.")

    sheet.status = PaymentSheet.Status.APPROVED
    sheet.approved_by = approved_by
    sheet.approved_at = timezone.now()
    sheet.save(update_fields=["status", "approved_by", "approved_at"])
    return sheet


def reject_sheet(sheet: PaymentSheet, rejected_by, reason: str):
    if not rejected_by.is_proprietor:
        raise PermissionDenied("Only the Proprietor can reject a payment sheet.")
    if not reason or not reason.strip():
        raise ValidationError("A rejection reason is required.")
    if sheet.status != PaymentSheet.Status.PENDING_APPROVAL:
        raise ValidationError("Only a sheet pending approval can be rejected.")

    sheet.status = PaymentSheet.Status.DRAFT
    sheet.rejection_reason = reason
    sheet.save(update_fields=["status", "rejection_reason"])
    return sheet


def sign_entry(entry: SalaryEntry, signed_by):
    """A teacher/staff member confirms receipt of their salary."""
    if entry.sheet.status != PaymentSheet.Status.APPROVED:
        raise ValidationError("Salary entries can only be signed once the sheet is approved.")
    entry.mark_signed()

    sheet = entry.sheet
    if not sheet.entries.filter(signed=False).exists():
        sheet.status = PaymentSheet.Status.DISBURSED
        sheet.save(update_fields=["status"])
    return entry
