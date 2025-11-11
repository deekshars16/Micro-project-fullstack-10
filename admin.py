from django.contrib import admin
from .models import Donor, BloodRequest

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'blood_group', 'city', 'available', 'last_donation')
    search_fields = ('full_name', 'city', 'phone', 'email')
    list_filter = ('blood_group', 'available')

@admin.register(BloodRequest)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('blood_group', 'units', 'city', 'urgent', 'created_at', 'fulfilled')
    list_filter = ('blood_group', 'urgent', 'fulfilled')
    search_fields = ('requester_name', 'city', 'phone', 'hospital_name')
