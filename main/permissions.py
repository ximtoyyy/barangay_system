"""WHO CAN OPEN WHAT. Every page uses one of these three decorators.
  @resident_required -> approved residents only
  @staff_required    -> approved staff (and admin)
  @admin_required    -> admin (superuser) only
Change access rules here, in one place.
"""
from functools import wraps
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect


def resident_required(view):
    @wraps(view)
    @login_required
    def wrapper(request, *args, **kwargs):
        res = getattr(request.user, "resident", None)
        if res is None:
            if request.user.is_staff:
                return redirect("home")
            logout(request)
            return redirect("login")
        if res.approval != "approved":
            logout(request)
            messages.error(request, "Your account is not approved.")
            return redirect("login")
        return view(request, *args, **kwargs)
    return wrapper


def staff_required(view):
    return login_required(user_passes_test(lambda u: u.is_staff, login_url="login")(view))


def admin_required(view):
    return login_required(user_passes_test(lambda u: u.is_superuser, login_url="login")(view))
