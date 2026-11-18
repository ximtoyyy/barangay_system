"""STAFF PAGES: request list (search/filter), manage one request, print the document."""
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import StatusForm
from main.certificates import certificate_template
from main.models import DocumentRequest, BarangaySetting
from main.notifications import notify_status_change
from main.permissions import staff_required


@staff_required
def staff_dashboard(request):
    reqs = DocumentRequest.objects.select_related("resident", "document_type")
    status = request.GET.get("status", "")
    q = request.GET.get("q", "")
    if status:
        reqs = reqs.filter(status=status)
    if q:
        reqs = reqs.filter(Q(reference_no__icontains=q) | Q(resident__full_name__icontains=q))
    return render(request, "staff/dashboard.html", {
        "requests": reqs, "status": status, "q": q, "choices": DocumentRequest.STATUS})


@staff_required
def staff_detail(request, pk):
    obj = get_object_or_404(DocumentRequest, pk=pk)
    old_status = obj.status
    form = StatusForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.handled_by = request.user          # remember which staff handled it
        if obj.payment_status == "paid":
            obj.paid_at = obj.paid_at or timezone.now()
        else:
            obj.paid_at = None
        obj.save()
        if obj.status != old_status and notify_status_change(obj):
            messages.success(request, f"Request updated. Email sent to {obj.resident.user.email}.")
        else:
            messages.success(request, "Request updated.")
        return redirect("staff_dashboard")
    return render(request, "staff/request_detail.html", {"r": obj, "form": form})


@staff_required
@require_POST
def mark_ready(request, pk):
    """One click: set status to Ready for Pickup and email the resident."""
    obj = get_object_or_404(DocumentRequest, pk=pk)
    if obj.status in ("ready", "released"):
        messages.info(request, f"{obj.reference_no} is already {obj.get_status_display()}.")
        return redirect("staff_dashboard")
    remarks = request.POST.get("remarks", "").strip()
    if remarks:
        obj.remarks = remarks
    obj.status = "ready"
    obj.handled_by = request.user
    obj.save()
    if notify_status_change(obj):
        messages.success(request, f"{obj.reference_no} marked Ready. Email sent to {obj.resident.user.email}.")
    else:
        messages.warning(request, f"{obj.reference_no} marked Ready, but the email could not be sent.")
    return redirect("staff_dashboard")


@staff_required
def print_document(request, pk):
    obj = get_object_or_404(DocumentRequest, pk=pk)
    return render(request, certificate_template(obj.document_type.name),
                  {"r": obj, "res": obj.resident, "b": BarangaySetting.load()})
