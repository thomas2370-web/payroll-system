from django.contrib import admin

from payroll.models import PaymentSheet, SalaryEntry


class SalaryEntryInline(admin.TabularInline):
    model = SalaryEntry
    extra = 0
    readonly_fields = ("staff_name", "amount", "adjusted_hours", "signed", "signed_at")
    can_delete = False


@admin.register(PaymentSheet)
class PaymentSheetAdmin(admin.ModelAdmin):
    list_display = ("month", "status", "submitted_by", "approved_by", "approved_at")
    list_filter = ("status",)
    inlines = [SalaryEntryInline]
