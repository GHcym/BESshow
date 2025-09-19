from django.urls import path
from .views import UserProfileDetailView, UserProfileUpdateView, AccountListView, AccountUpdateView, AccountCreateView, toggle_account_status # Import AccountUpdateView and AccountCreateView

urlpatterns = [
    path('profile/', UserProfileDetailView.as_view(), name='user_profile_detail'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='user_profile_update'),
    path('list/', AccountListView.as_view(), name='account_list'),
    path('create/', AccountCreateView.as_view(), name='account_create'), # New URL for creating accounts
    path('<int:pk>/edit/', AccountUpdateView.as_view(), name='account_update'), # New URL
    path('<int:pk>/toggle-status/', toggle_account_status, name='toggle_account_status'), # New URL for toggling account status
]
