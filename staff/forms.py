from django import forms

from staff.models import FixedStaff, Teacher


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ["name", "subject", "hourly_rate", "expected_weekly_hours"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "hourly_rate": forms.NumberInput(attrs={"class": "form-control"}),
            "expected_weekly_hours": forms.NumberInput(attrs={"class": "form-control"}),
        }


class FixedStaffForm(forms.ModelForm):
    class Meta:
        model = FixedStaff
        fields = ["name", "role_title", "fixed_salary"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "role_title": forms.TextInput(attrs={"class": "form-control"}),
            "fixed_salary": forms.NumberInput(attrs={"class": "form-control"}),
        }
