"""RESIDENT FORMS: the document request form and the QR Ph proof-of-payment form."""
from django import forms
from main.models import DocumentRequest, BarangaySetting


class RequestForm(forms.ModelForm):
    class Meta:
        model = DocumentRequest
        fields = ["document_type", "payment_method", "purpose", "details", "attachment"]
        labels = {"document_type": "Document", "payment_method": "How will you pay?", "purpose": "Purpose",
                  "details": "Other details (if needed)", "attachment": "Valid ID / proof (photo or PDF)"}
        widgets = {
            "payment_method": forms.RadioSelect(attrs={"class": "choice-list"}),
            "details": forms.Textarea(attrs={"rows": 2, "placeholder": "Example: name of the child, business name, relationship"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not BarangaySetting.load().qr_ready:      # no QR uploaded by the admin yet -> cash only
            self.fields["payment_method"].choices = [c for c in DocumentRequest.METHODS if c[0] == "cash"]


class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = DocumentRequest
        fields = ["payment_reference", "payment_proof"]
        labels = {"payment_reference": "Reference number (from your payment app)",
                  "payment_proof": "Screenshot of your payment"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["payment_reference"].required = True
        self.fields["payment_proof"].required = True
