from django.utils import timezone

from attendance.models import AttendanceRecord
from staff.models import Teacher


class InvalidQRCode(Exception):
    pass


def scan_check_in(qr_token, scanned_by):
    """Called when the Discipline Master scans a teacher's QR code on arrival."""
    teacher = _resolve_teacher(qr_token)
    record, _ = AttendanceRecord.objects.get_or_create(
        teacher=teacher,
        session_date=timezone.localdate(),
    )
    record.check_in = timezone.now()
    record.scanned_by = scanned_by
    record.save(update_fields=["check_in", "scanned_by"])
    return record


def scan_check_out(qr_token, scanned_by):
    """Called when the Discipline Master scans a teacher's QR code on departure."""
    teacher = _resolve_teacher(qr_token)
    try:
        record = AttendanceRecord.objects.get(
            teacher=teacher, session_date=timezone.localdate()
        )
    except AttendanceRecord.DoesNotExist:
        raise InvalidQRCode("No check-in found for today. Scan check-in first.")

    record.check_out = timezone.now()
    record.save(update_fields=["check_out"])
    return record


def _resolve_teacher(qr_token):
    try:
        return Teacher.objects.get(qr_token=qr_token, is_active=True)
    except Teacher.DoesNotExist:
        raise InvalidQRCode("QR code not recognised or teacher is inactive.")
