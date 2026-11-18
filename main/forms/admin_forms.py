"""ADMIN FORMS: the Barangay Settings form (name, officials, certificate look, QR Ph)."""
from django import forms
from main.models import BarangaySetting


class BarangaySettingForm(forms.ModelForm):
    class Meta:
        model = BarangaySetting
        fields = ["barangay_name", "municipality", "province", "punong_barangay", "certificate_style",
                  "logo_image", "logo2_image", "qr_image", "qr_account_name", "qr_note"]
