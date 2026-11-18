"""LOGIN + REGISTRATION FORMS (public pages).
Edit here to change the fields on the resident sign-up, staff sign-up, or the login rules.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from main.models import Resident, StaffProfile


class EmailLoginForm(AuthenticationForm):
    username = forms.CharField(label="Email (staff may use username)")

    def confirm_login_allowed(self, user):
        """Block login until the admin approved the account."""
        super().confirm_login_allowed(user)
        profile = getattr(user, "resident", None) or getattr(user, "staffprofile", None)
        if profile and profile.approval != "approved":
            if profile.approval == "rejected":
                msg = "Your registration was not approved. Please contact the barangay office."
            else:
                msg = "Your account is still waiting for admin approval. You will receive an email once approved."
            raise forms.ValidationError(msg, code="not_approved")


class _EmailUniqueMixin:
    def clean_email(self):
        e = self.cleaned_data["email"].lower()
        if User.objects.filter(username=e).exists():
            raise forms.ValidationError("This email is already registered.")
        return e


class RegisterForm(_EmailUniqueMixin, forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    full_name = forms.CharField(max_length=150)
    birthdate = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    address = forms.CharField(max_length=255)
    purok = forms.CharField(max_length=50, required=False)
    contact_no = forms.CharField(max_length=20)

    def save(self):
        d = self.cleaned_data
        user = User.objects.create_user(d["email"], email=d["email"], password=d["password"])
        Resident.objects.create(
            user=user, full_name=d["full_name"], birthdate=d["birthdate"],
            address=d["address"], purok=d["purok"], contact_no=d["contact_no"])
        return user


class StaffRegisterForm(_EmailUniqueMixin, forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    full_name = forms.CharField(max_length=150)
    position = forms.CharField(max_length=100, required=False, label="Position (e.g. Secretary, Clerk)")
    contact_no = forms.CharField(max_length=20)

    def save(self):
        d = self.cleaned_data
        # is_staff stays False until the admin approves
        user = User.objects.create_user(d["email"], email=d["email"], password=d["password"],
                                        first_name=d["full_name"][:150])
        StaffProfile.objects.create(user=user, full_name=d["full_name"],
                                    position=d["position"], contact_no=d["contact_no"])
        return user
