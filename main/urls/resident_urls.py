"""RESIDENT URLS."""
from django.urls import path
from main.views import resident

urlpatterns = [
    path("my/", resident.dashboard, name="dashboard"),
    path("request/new/", resident.new_request, name="new_request"),
    path("request/<int:pk>/", resident.request_detail, name="request_detail"),
    path("request/<int:pk>/pay/", resident.submit_payment, name="submit_payment"),
]
