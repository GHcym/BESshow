from django.shortcuts import render
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import CustomUser
from .forms import CustomUserUpdateForm

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'account/user_profile_detail.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'account/user_profile_form.html'
    context_object_name = 'user_profile'
    success_url = reverse_lazy('user_profile_detail') # Redirect to profile detail after update

    def get_object(self):
        return self.request.user
