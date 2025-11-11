from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from phonenumber_field.modelfields import PhoneNumberField

BLOOD_GROUPS = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-'),
]

def default_last_donation():
    # default to a long time ago so new donors are eligible by default
    return timezone.now().date() - timedelta(days=365)

class Donor(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    full_name = models.CharField(max_length=120)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    phone = PhoneNumberField()  # requires django-phonenumber-field
    email = models.EmailField(blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_donation = models.DateField(default=default_last_donation)
    available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} ({self.blood_group})"

    @property
    def days_since_donation(self):
        return (timezone.now().date() - self.last_donation).days

    def is_eligible(self, min_days=90):
        """Return True if donor is marked available and last donation was at least min_days ago."""
        return self.available and self.days_since_donation >= min_days


class BloodRequest(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    requester_name = models.CharField(max_length=120)
    phone = PhoneNumberField()
    email = models.EmailField(blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    units = models.PositiveIntegerField(default=1)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    hospital_name = models.CharField(max_length=200, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    urgent = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"Request {self.blood_group} ×{self.units} in {self.city} ({'URGENT' if self.urgent else 'Normal'})"
