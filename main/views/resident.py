"""RESIDENT PAGES: My Requests, New Request, Request Detail (+ sending QR Ph proof of payment)."""
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.forms import RequestForm, PaymentProofForm
from main.models import DocumentRequest, BarangaySetting
from main.notifications import notify_new_request, notify_payment_proof
from main.permissions import resident_required


@resident_required
def dashboard(request):
    reqs = DocumentRequest.objects.filter(resident__user=request.user)
    return render(request, "resident/dashboard.html", {"requests": reqs})


@resident_required
def new_request(request):
    form = RequestForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.resident = request.user.resident
        obj.save()
        emailed = notify_new_request(obj)
        msg = f"Request submitted and sent to the barangay. Reference no: {obj.reference_no}."
        if not emailed:
            msg += " (We could not send the confirmation email, but your request was received.)"
        pay_online = obj.payment_method == "qrph" and obj.fee_charged > 0
        if pay_online:
            msg += " Next: pay with the QR Ph code below."
        messages.success(request, msg)
        return redirect("request_detail", pk=obj.pk) if pay_online else redirect("dashboard")
    return render(request, "resident/request_form.html", {"form": form, "qr_ready": BarangaySetting.load().qr_ready})


def _detail(request, obj, proof_form=None):
    if proof_form is None and obj.can_submit_proof:
        proof_form = PaymentProofForm()
    return render(request, "resident/request_detail.html",
                  {"r": obj, "b": BarangaySetting.load(), "proof_form": proof_form})


@resident_required
def request_detail(request, pk):
    return _detail(request, get_object_or_404(DocumentRequest, pk=pk, resident__user=request.user))


@resident_required
@require_POST
def submit_payment(request, pk):
    """Resident sends the screenshot + reference number after paying through QR Ph."""
    obj = get_object_or_404(DocumentRequest, pk=pk, resident__user=request.user)
    if not obj.can_submit_proof:
        messages.error(request, "This request does not need an online payment.")
        return redirect("request_detail", pk=pk)
    form = PaymentProofForm(request.POST, request.FILES, instance=obj)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.payment_status = "verifying"
        obj.save()
        notify_payment_proof(obj)
        messages.success(request, "Payment proof sent. Staff will check it and mark your request as paid.")
        return redirect("request_detail", pk=pk)
    return _detail(request, obj, proof_form=form)
