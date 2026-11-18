"""BARANGAY SETTINGS (only one row). Fill it in once at /admin/ > Barangay settings:
the barangay name, officials for the certificates, and the QR Ph code residents scan to pay online."""
from django.db import models


class BarangaySetting(models.Model):
    barangay_name = models.CharField(max_length=100, blank=True, help_text="Example: San Isidro")
    municipality = models.CharField("Municipality / City", max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    punong_barangay = models.CharField("Punong Barangay (name)", max_length=150, blank=True)
    STYLES = [("blue", "Royal Blue"), ("classic", "Classic Gold"), ("green", "Forest Green")]
    certificate_style = models.CharField("Certificate colour style", max_length=10, choices=STYLES, default="blue",
                                         help_text="Staff can still switch the style on the print page.")
    logo_image = models.FileField("Barangay logo / seal (left side)", upload_to="logos/", blank=True)
    logo2_image = models.FileField("Municipality / city logo (right side)", upload_to="logos/", blank=True,
                                   help_text="Optional.")
    qr_image = models.FileField("QR Ph code (image)", upload_to="qr/", blank=True,
                                help_text="Upload the barangay's QR Ph code. Leave empty to accept cash only.")
    qr_account_name = models.CharField("Account name shown with the QR", max_length=150, blank=True)
    qr_note = models.CharField("Note shown with the QR", max_length=255, blank=True,
                               help_text="Example: Scan with GCash, Maya or any bank app that supports QR Ph")

    class Meta:
        verbose_name = "Barangay setting"
        verbose_name_plural = "Barangay settings"

    def __str__(self):
        return "Barangay settings"

    @classmethod
    def load(cls):
        return cls.objects.first() or cls()

    @property
    def qr_ready(self):
        return bool(self.qr_image)
