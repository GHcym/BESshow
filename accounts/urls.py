from django.urls import path
from .views import UserProfileDetailView, UserProfileUpdateView, AccountListView, AccountUpdateView # Import AccountUpdateView

urlpatterns = [
    path('profile/', UserProfileDetailView.as_view(), name='user_profile_detail'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='user_profile_update'),
    path('list/', AccountListView.as_view(), name='account_list'),
    path('<int:pk>/edit/', AccountUpdateView.as_view(), name='account_update'), # New URL
]
