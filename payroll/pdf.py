"""
Generates the printable, signable payment sheet PDF for a given
PaymentSheet, as described in section 3.2 (Payment Sheet Module).
"""
from django.template.loader import render_to_string
from weasyprint import HTML

from payroll.models import PaymentSheet


def render_payment_sheet_pdf(sheet: PaymentSheet) -> bytes:
    html_string = render_to_string("payroll/payment_sheet_pdf.html", {
        "sheet": sheet,
        "entries": sheet.entries.select_related("teacher", "fixed_staff").all(),
        "total": sum(e.amount for e in sheet.entries.all()),
    })
    return HTML(string=html_string).write_pdf()
