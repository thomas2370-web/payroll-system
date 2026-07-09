from django.contrib import admin

from staff.models import FixedStaff, Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "hourly_rate", "expected_weekly_hours", "is_active")
    list_filter = ("is_active", "subject")
    search_fields = ("name",)
    readonly_fields = ("qr_token", "qr_image")


@admin.register(FixedStaff)
class FixedStaffAdmin(admin.ModelAdmin):
    list_display = ("name", "role_title", "fixed_salary", "is_active")
    list_filter = ("is_active",)
