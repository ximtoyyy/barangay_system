"""ADMIN PAGES: dashboard, approve/reject STAFF accounts, user activity (last login)."""
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.forms import BarangaySettingForm
from main.models import BarangaySetting
from main.models import Resident, StaffProfile, DocumentRequest
from main.notifications import notify_account_decision
from main.permissions import admin_required


@admin_required
def admin_dashboard(request):
    counts = {k: 0 for k, _ in DocumentRequest.STATUS}
    for s in DocumentRequest.objects.values_list("status", flat=True):
        counts[s] += 1
    return render(request, "manage/dashboard.html", {
        "status_counts": [(label, counts[k]) for k, label in DocumentRequest.STATUS],
        "total_requests": sum(counts.values()),
        "pending_staff": StaffProfile.objects.filter(approval="pending").count(),
        "total_residents": Resident.objects.filter(approval="approved").count(),
        "total_staff": User.objects.filter(is_staff=True, is_superuser=False).count(),
        "recent_requests": DocumentRequest.objects.select_related("resident", "document_type")[:5],
        "recent_logins": User.objects.exclude(last_login=None).order_by("-last_login")[:5]})


@admin_required
def accounts(request):
    """Staff sign-ups waiting for the admin's approval."""
    status = request.GET.get("status", "pending")
    qs = StaffProfile.objects.select_related("user").order_by("-date_registered")
    if status != "all":
        qs = qs.filter(approval=status)
    return render(request, "manage/accounts.html", {
        "items": qs, "status": status,
        "pending_staff": StaffProfile.objects.filter(approval="pending").count()})


@admin_required
@require_POST
def account_action(request, pk, action):
    staff = get_object_or_404(StaffProfile, pk=pk)
    if action in ("approve", "reject"):
        staff.approval = "approved" if action == "approve" else "rejected"
        staff.save()
        staff.user.is_staff = staff.approval == "approved"   # staff powers only when approved
        staff.user.save()
        notify_account_decision(staff, "staff")
        messages.success(request, f"{staff.full_name}: account {staff.approval}. Email sent to {staff.user.email}.")
    return redirect("accounts")


@admin_required
def user_activity(request):
    role, q = request.GET.get("role", ""), request.GET.get("q", "")
    users = User.objects.select_related("resident").order_by(F("last_login").desc(nulls_last=True))
    if role == "staff":
        users = users.filter(is_staff=True)
    elif role == "resident":
        users = users.filter(is_staff=False)
    if q:
        users = users.filter(username__icontains=q)
    return render(request, "manage/user_activity.html", {"users": users, "role": role, "q": q})


@admin_required
def barangay_settings(request):
    """Change the barangay name, officials, logos, certificate style and QR Ph code."""
    form = BarangaySettingForm(request.POST or None, request.FILES or None, instance=BarangaySetting.objects.first())
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Barangay settings saved.")
        return redirect("barangay_settings")
    return render(request, "manage/barangay_settings.html", {"form": form})
