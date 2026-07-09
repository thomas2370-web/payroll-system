from django.contrib import admin

from attendance.models import Adjustment, AttendanceRecord


class AdjustmentInline(admin.TabularInline):
    model = Adjustment
    extra = 0


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("teacher", "session_date", "check_in", "check_out", "hours_worked")
    list_filter = ("session_date",)
    search_fields = ("teacher__name",)
    inlines = [AdjustmentInline]


@admin.register(Adjustment)
class AdjustmentAdmin(admin.ModelAdmin):
    list_display = ("teacher", "attendance_record", "deduct_hours", "recorded_by", "created_at")
    search_fields = ("teacher__name",)
