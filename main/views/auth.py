"""PUBLIC PAGES: home redirect (sends each role to its own page), resident sign-up, staff sign-up.
(The login page itself is Django's LoginView, set in urls/auth_urls.py.)
"""
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from main.forms import RegisterForm, StaffRegisterForm
from main.notifications import notify_new_registration


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.is_superuser:
        return redirect("admin_dashboard")
    return redirect("staff_dashboard" if request.user.is_staff else "dashboard")


def register(request):
    """Residents sign up and can use the system right away (no approval needed)."""
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome! Your account is ready. You can now request documents.")
        return redirect("home")
    return render(request, "registration/register.html", {"form": form})


def staff_register(request):
    form = StaffRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        notify_new_registration(user.staffprofile, "staff")
        messages.success(request, "Staff account created. Please wait for the admin to approve it. "
                                  "You will receive an email once approved.")
        return redirect("login")
    return render(request, "registration/staff_register.html", {"form": form})
