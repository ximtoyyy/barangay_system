"""PUBLIC URLS: login, logout, register, home."""
from django.contrib.auth import views as auth_views
from django.urls import path
from main.forms import EmailLoginForm
from main.views import auth

urlpatterns = [
    path("", auth.home, name="home"),
    path("register/", auth.register, name="register"),
    path("register/staff/", auth.staff_register, name="staff_register"),
    path("login/", auth_views.LoginView.as_view(authentication_form=EmailLoginForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
