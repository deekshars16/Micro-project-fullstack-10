from django import forms
from .models import Donor, BloodRequest

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = [
            'full_name', 'blood_group', 'phone', 'email',
            'city', 'state', 'latitude', 'longitude',
            'last_donation', 'available', 'notes'
        ]
        widgets = {
            'last_donation': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = [
            'requester_name', 'phone', 'email',
            'blood_group', 'units', 'city', 'state',
            'hospital_name', 'urgent', 'message'
        ]
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
