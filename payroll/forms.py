from django import forms


class GenerateSheetForm(forms.Form):
    month = forms.DateField(
        label="Month (any date within the target month)",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )


class RejectSheetForm(forms.Form):
    reason = forms.CharField(
        label="Reason for rejection",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )
