"""STAFF FORMS: the form staff use to update a request's status and remarks."""
from django import forms
from main.models import DocumentRequest


class StatusForm(forms.ModelForm):
    class Meta:
        model = DocumentRequest
        fields = ["status", "payment_method", "payment_status", "remarks"]
        labels = {"payment_status": "Fee payment", "payment_method": "Payment method"}
        widgets = {"remarks": forms.Textarea(attrs={"rows": 3})}
