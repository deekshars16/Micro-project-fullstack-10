from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from .forms import SignUpForm, DonorForm, BloodRequestForm
from .models import Donor, BloodRequest
from django.views.generic import DetailView

class WelcomeView(TemplateView):
    template_name = 'bloodapp/welcome.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donor_count'] = Donor.objects.filter(available=True).count()
        context['request_count'] = BloodRequest.objects.filter(fulfilled=False).count()
        return context

class BloodRequestCreateView(LoginRequiredMixin, CreateView):
    model = BloodRequest
    form_class = BloodRequestForm
    template_name = 'bloodapp/request_form.html'
    success_url = reverse_lazy('bloodapp:donor_list')

class DonorListView(ListView):
    model = Donor
    template_name = 'bloodapp/donor_list.html'
    context_object_name = 'donors'
    
    def get_queryset(self):
        """Return all available donors."""
        return Donor.objects.filter(available=True).order_by('-created_at')

class UserLoginView(LoginView):
    template_name = 'bloodapp/login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('bloodapp:welcome')

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'bloodapp/signup.html'
    success_url = reverse_lazy('bloodapp:donor_list')

    def form_valid(self, form):
        # Save user and log them in automatically
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

from django.contrib import messages
from django.shortcuts import redirect

class DonorCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('bloodapp:login')
    model = Donor
    form_class = DonorForm
    template_name = 'bloodapp/donor_form.html'
    success_url = reverse_lazy('bloodapp:donor_list')

    def form_valid(self, form):
        """Attach the logged-in user to the donor record and prevent duplicates."""
        # If the user already has a donor profile, don't create another one.
        if Donor.objects.filter(user=self.request.user).exists():
            messages.warning(self.request, "You already have a donor profile.")
            return redirect(self.success_url)

        form.instance.user = self.request.user
        return super().form_valid(form)


class MyDonorView(LoginRequiredMixin, DetailView):
    """Show the current user's donor profile; redirect to create if none."""
    model = Donor
    template_name = 'bloodapp/my_donor.html'
    context_object_name = 'donor'

    def get_object(self, queryset=None):
        try:
            return Donor.objects.get(user=self.request.user)
        except Donor.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            messages.info(request, 'You do not have a donor profile yet. Please register.')
            return redirect('bloodapp:donor_create')
        return super().get(request, *args, **kwargs)


class MyRequestsListView(LoginRequiredMixin, ListView):
    model = BloodRequest
    template_name = 'bloodapp/my_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return BloodRequest.objects.filter(user=self.request.user).order_by('-created_at')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'bloodapp/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user's donor profile (if any)
        try:
            donor = Donor.objects.get(user=self.request.user)
        except Donor.DoesNotExist:
            donor = None
        # recent requests by this user
        requests = BloodRequest.objects.filter(user=self.request.user).order_by('-created_at')[:5]
        context['donor'] = donor
        context['requests'] = requests
        return context


class MapsView(TemplateView):
    template_name = 'bloodapp/maps.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.core.serializers import serialize
        import json
        from django.conf import settings
        
        # Get all available donors
        donors = Donor.objects.filter(available=True)
        # Get active blood requests
        requests = BloodRequest.objects.filter(fulfilled=False)
        
        # Convert querysets to JSON
        donors_json = json.loads(serialize('json', donors))
        requests_json = json.loads(serialize('json', requests))
        
        # Extract the fields we need
        donors_list = [
            {
                'full_name': donor['fields']['full_name'],
                'blood_group': donor['fields']['blood_group'],
                'city': donor['fields']['city'],
                'available': donor['fields']['available'],
                'latitude': str(donor['fields']['latitude']),
                'longitude': str(donor['fields']['longitude'])
            }
            for donor in donors_json
        ]
        
        requests_list = [
            {
                'blood_group': req['fields']['blood_group'],
                'units': req['fields']['units'],
                'city': req['fields']['city'],
                'hospital_name': req['fields']['hospital_name'],
                'urgent': req['fields']['urgent'],
                'latitude': str(req['fields']['latitude']),
                'longitude': str(req['fields']['longitude'])
            }
            for req in requests_json
        ]
        
        context['donors_json'] = json.dumps(donors_list)
        context['requests_json'] = json.dumps(requests_list)
        context['blood_groups'] = Donor._meta.get_field('blood_group').choices
        context['google_maps_api_key'] = getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
        
        return context
