from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.permissions import role_required
from attendance.forms import AdjustmentForm, ScanForm
from attendance.models import Adjustment, AttendanceRecord
from attendance.services import InvalidQRCode, scan_check_in, scan_check_out
from staff.models import Teacher


@login_required
@role_required("DISCIPLINE_MASTER")
def scan(request):
    """
    One shared scan page with two buttons (Check in / Check out).
    A JS QR reader can auto-submit this form once it decodes a code;
    the qr_token field also accepts manual entry.
    """
    form = ScanForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        action = request.POST.get("action")
        token = form.cleaned_data["qr_token"]
        try:
            if action == "check_out":
                record = scan_check_out(token, scanned_by=request.user)
                messages.success(request, f"Check-out recorded for {record.teacher.name} at {record.check_out:%H:%M}.")
            else:
                record = scan_check_in(token, scanned_by=request.user)
                messages.success(request, f"Check-in recorded for {record.teacher.name} at {record.check_in:%H:%M}.")
        except InvalidQRCode as exc:
            messages.error(request, str(exc))
        form = ScanForm()
    return render(request, "attendance/scan.html", {"form": form})


@login_required
@role_required("DISCIPLINE_MASTER", "PRINCIPAL")
def log(request):
    records = AttendanceRecord.objects.select_related("teacher").order_by("-session_date")[:100]
    return render(request, "attendance/log.html", {"records": records})


@login_required
@role_required("DISCIPLINE_MASTER")
def add_adjustment(request, record_id):
    record = get_object_or_404(AttendanceRecord, pk=record_id)
    if request.method == "POST":
        form = AdjustmentForm(request.POST)
        if form.is_valid():
            adjustment = form.save(commit=False)
            adjustment.teacher = record.teacher
            adjustment.attendance_record = record
            adjustment.recorded_by = request.user
            adjustment.save()
            messages.success(request, f"Penalty of {adjustment.deduct_hours}h recorded for {record.teacher.name}.")
            return redirect("attendance:log")
    else:
        form = AdjustmentForm()
    return render(request, "attendance/add_adjustment.html", {"form": form, "record": record})


@login_required
@role_required("DISCIPLINE_MASTER", "PRINCIPAL")
def teacher_adjustment_history(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    adjustments = (
        Adjustment.objects.filter(teacher=teacher)
        .select_related("attendance_record", "recorded_by")
        .order_by("-created_at")
    )
    total_deducted = sum(adjustment.deduct_hours for adjustment in adjustments)
    return render(
        request,
        "attendance/teacher_adjustment_history.html",
        {"teacher": teacher, "adjustments": adjustments, "total_deducted": total_deducted},
    )
