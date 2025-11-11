from django.urls import path
from . import views

app_name = 'bloodapp'  # Required for namespace in project urls.py

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('donor/new/', views.DonorCreateView.as_view(), name='donor_create'),
    path('request/new/', views.BloodRequestCreateView.as_view(), name='request_add'),
    path('my/donor/', views.MyDonorView.as_view(), name='my_donor'),
    path('my/requests/', views.MyRequestsListView.as_view(), name='my_requests'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('donors/', views.DonorListView.as_view(), name='donor_list'),
    path('maps/', views.MapsView.as_view(), name='maps'),
    path('', views.WelcomeView.as_view(), name='welcome')
]