from django.urls import path
from .views import UserProfileDetailView, UserProfileUpdateView

urlpatterns = [
    path('profile/', UserProfileDetailView.as_view(), name='user_profile_detail'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='user_profile_update'),
]
