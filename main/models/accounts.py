"""ACCOUNT TABLES: Resident and StaffProfile (the profile + approval status of each person).
Edit this file to add/remove fields on resident or staff accounts.
After editing, run: python manage.py makemigrations main  then  python manage.py migrate
"""
from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    birthdate = models.DateField()
    address = models.CharField(max_length=255)
    purok = models.CharField(max_length=50, blank=True)
    contact_no = models.CharField(max_length=20)
    APPROVAL = [("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")]
    approval = models.CharField(max_length=10, choices=APPROVAL, default="approved")  # residents need no approval
    date_registered = models.DateTimeField(default=timezone.now)

    @property
    def age(self):
        today, b = date.today(), self.birthdate
        return today.year - b.year - ((today.month, today.day) < (b.month, b.day))

    def __str__(self):
        return self.full_name


class StaffProfile(models.Model):
    """Staff who sign up themselves. They cannot log in until the admin approves."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    contact_no = models.CharField(max_length=20)
    position = models.CharField(max_length=100, blank=True)  # e.g. Secretary, Clerk
    approval = models.CharField(max_length=10, choices=Resident.APPROVAL, default="pending")
    date_registered = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name
