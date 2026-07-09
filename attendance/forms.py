from django import forms

from attendance.models import Adjustment


class ScanForm(forms.Form):
    """
    In production, `qr_token` is populated by a JS QR-scanning library
    (e.g. html5-qrcode) reading the camera feed and submitting the
    decoded value here. The text field also allows manual entry as a
    fallback if a camera isn't available.
    """
    qr_token = forms.CharField(
        label="Scanned QR token",
        widget=forms.TextInput(attrs={"class": "form-control", "autofocus": True}),
    )


class AdjustmentForm(forms.ModelForm):
    class Meta:
        model = Adjustment
        fields = ["deduct_hours", "justification"]
        widgets = {
            "deduct_hours": forms.NumberInput(attrs={"class": "form-control", "step": "0.25"}),
            "justification": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
