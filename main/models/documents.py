"""DOCUMENT TABLES: DocumentType (what can be requested + fee) and DocumentRequest (each request).
Edit this file to add fields to requests, or to change the list of statuses.
After editing, run: python manage.py makemigrations main  then  python manage.py migrate
"""
import uuid
from django.contrib.auth.models import User
from django.db import models
from .accounts import Resident


class DocumentType(models.Model):
    name = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    requirements = models.TextField(blank=True)

    def __str__(self):
        return self.name


def make_reference():
    return "BRGY-" + uuid.uuid4().hex[:8].upper()


class DocumentRequest(models.Model):
    STATUS = [
        ("pending", "Pending"), ("review", "Under Review"), ("approved", "Approved"),
        ("rejected", "Rejected"), ("ready", "Ready for Pickup"), ("released", "Released"),
    ]
    reference_no = models.CharField(max_length=20, unique=True, default=make_reference)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)
    purpose = models.CharField(max_length=255)
    details = models.TextField(blank=True)   # names / business name etc. printed on some certificates
    attachment = models.FileField(upload_to="requests/", blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    remarks = models.TextField(blank=True)
    PAYMENT = [("unpaid", "Unpaid"), ("verifying", "Verifying payment"), ("paid", "Paid"), ("free", "Free")]
    METHODS = [("cash", "Cash (pay at the Barangay Hall)"), ("qrph", "Pay online via QR Ph")]
    fee_charged = models.DecimalField(max_digits=8, decimal_places=2, default=0)   # fee at the time of the request
    payment_status = models.CharField(max_length=10, choices=PAYMENT, default="unpaid")
    paid_at = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=10, choices=METHODS, default="cash")
    payment_reference = models.CharField("QR Ph reference no.", max_length=60, blank=True)
    payment_proof = models.FileField("Screenshot of payment", upload_to="payments/", blank=True)
    handled_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="handled_requests")  # staff who last updated it
    date_requested = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_requested"]

    def save(self, *args, **kwargs):
        if self._state.adding and not self.fee_charged:      # new request: copy the document's fee
            self.fee_charged = self.document_type.fee
            self.payment_status = "free" if self.fee_charged == 0 else "unpaid"
        super().save(*args, **kwargs)

    @property
    def fee_label(self):
        return "Free" if self.fee_charged == 0 else f"₱{self.fee_charged:,.2f}"

    @property
    def method_short(self):
        return "QR Ph" if self.payment_method == "qrph" else "Cash"

    @property
    def can_submit_proof(self):
        """True while a QR Ph payer may still send (or re-send) a payment screenshot."""
        return self.payment_method == "qrph" and self.fee_charged > 0 and self.payment_status in ("unpaid", "verifying")

    @property
    def handler_name(self):
        """Name of the staff member who handled this request (empty if nobody yet)."""
        u = self.handled_by
        if not u:
            return ""
        profile = getattr(u, "staffprofile", None)
        return (profile.full_name if profile else u.get_full_name()) or u.username

    def __str__(self):
        return f"{self.reference_no} - {self.document_type}"
