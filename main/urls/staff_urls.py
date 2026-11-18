"""STAFF URLS (all start with /staff/)."""
from django.urls import path
from main.views import staff

urlpatterns = [
    path("staff/", staff.staff_dashboard, name="staff_dashboard"),
    path("staff/request/<int:pk>/", staff.staff_detail, name="staff_detail"),
    path("staff/request/<int:pk>/ready/", staff.mark_ready, name="mark_ready"),
    path("staff/request/<int:pk>/print/", staff.print_document, name="print_document"),
]
