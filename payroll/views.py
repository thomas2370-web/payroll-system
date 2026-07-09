import calendar
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.permissions import role_required
from payroll.forms import GenerateSheetForm, RejectSheetForm
from payroll.models import PaymentSheet, SalaryEntry
from payroll.services import (
    approve_sheet,
    generate_payment_sheet,
    reject_sheet,
    sign_entry,
    submit_for_approval,
)


@login_required
@role_required("ACCOUNTANT", "PROPRIETOR")
def sheet_list(request):
    if request.method == "POST" and request.user.is_accountant:
        form = GenerateSheetForm(request.POST)
        if form.is_valid():
            chosen = form.cleaned_data["month"]
            month_start = chosen.replace(day=1)
            month_end = date(chosen.year, chosen.month, calendar.monthrange(chosen.year, chosen.month)[1])
            try:
                sheet = generate_payment_sheet(month_start, month_end, submitted_by=request.user)
                messages.success(request, f"Payment sheet generated for {month_start:%B %Y}.")
                return redirect("payroll:sheet_detail", pk=sheet.pk)
            except ValidationError as exc:
                messages.error(request, str(exc))
    else:
        form = GenerateSheetForm()

    sheets = PaymentSheet.objects.order_by("-month")
    return render(request, "payroll/sheet_list.html", {"sheets": sheets, "form": form})


@login_required
@role_required("ACCOUNTANT", "PROPRIETOR")
def sheet_detail(request, pk):
    sheet = get_object_or_404(PaymentSheet, pk=pk)

    if request.method == "POST":
        action = request.POST.get("action")
        try:
            if action == "submit" and request.user.is_accountant:
                submit_for_approval(sheet, request.user)
                messages.success(request, "Sheet submitted to the Proprietor for approval.")
            elif action == "approve" and request.user.is_proprietor:
                approve_sheet(sheet, request.user)
                messages.success(request, "Sheet approved. Staff may now sign for payment.")
            elif action == "reject" and request.user.is_proprietor:
                reject_form = RejectSheetForm(request.POST)
                if reject_form.is_valid():
                    reject_sheet(sheet, request.user, reject_form.cleaned_data["reason"])
                    messages.warning(request, "Sheet rejected and returned to the Accountant.")
            else:
                raise PermissionDenied("Action not permitted for your role.")
        except (PermissionDenied, ValidationError) as exc:
            messages.error(request, str(exc))
        return redirect("payroll:sheet_detail", pk=sheet.pk)

    entries = sheet.entries.select_related("teacher", "fixed_staff").all()
    total = sum(e.amount for e in entries)
    reject_form = RejectSheetForm()
    return render(request, "payroll/sheet_detail.html", {
        "sheet": sheet, "entries": entries, "total": total, "reject_form": reject_form,
    })


@login_required
@role_required("ACCOUNTANT", "PROPRIETOR")
def sheet_pdf(request, pk):
    from payroll.pdf import render_payment_sheet_pdf
    sheet = get_object_or_404(PaymentSheet, pk=pk)
    pdf_bytes = render_payment_sheet_pdf(sheet)
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="payment_sheet_{sheet.month:%Y_%m}.pdf"'
    return response


@login_required
@role_required("TEACHER")
def my_payslips(request):
    entries = SalaryEntry.objects.filter(
        teacher__user=request.user
    ).select_related("sheet").order_by("-sheet__month")

    if request.method == "POST":
        entry = get_object_or_404(SalaryEntry, pk=request.POST.get("entry_id"), teacher__user=request.user)
        try:
            sign_entry(entry, request.user)
            messages.success(request, "Payment receipt confirmed.")
        except ValidationError as exc:
            messages.error(request, str(exc))
        return redirect("payroll:my_payslips")

    return render(request, "payroll/my_payslips.html", {"entries": entries})
