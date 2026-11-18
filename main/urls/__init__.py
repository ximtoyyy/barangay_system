"""Combines the URL files of every role. To add a page, add it in the matching *_urls.py file."""
from .auth_urls import urlpatterns as auth_urls
from .resident_urls import urlpatterns as resident_urls
from .staff_urls import urlpatterns as staff_urls
from .admin_urls import urlpatterns as admin_urls

urlpatterns = auth_urls + resident_urls + staff_urls + admin_urls
