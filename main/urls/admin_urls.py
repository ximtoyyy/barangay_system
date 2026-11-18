"""ADMIN URLS (all start with /manage/)."""
from django.urls import path
from main.views import admin_panel

urlpatterns = [
    path("manage/", admin_panel.admin_dashboard, name="admin_dashboard"),
    path("manage/accounts/", admin_panel.accounts, name="accounts"),
    path("manage/accounts/<int:pk>/<str:action>/", admin_panel.account_action, name="account_action"),
    path("manage/settings/", admin_panel.barangay_settings, name="barangay_settings"),
    path("manage/users/", admin_panel.user_activity, name="user_activity"),
]
