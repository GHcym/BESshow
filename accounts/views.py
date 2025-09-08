from django.shortcuts import render
from django.views.generic import DetailView, UpdateView, ListView # Import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Import UserPassesTestMixin for staff check
from django.urls import reverse_lazy, reverse

from .models import CustomUser
from .forms import CustomUserUpdateForm, AccountUpdateForm # Import AccountUpdateForm

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

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        print(f"DEBUG: next_url in get_success_url: {next_url}") # Debug print
        if next_url == 'payment':
            # Placeholder for the payment page URL
            return reverse('orders:payment_page') 
        else:
            return reverse('user_profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        return context

    def get_object(self):
        return self.request.user

class AccountListView(LoginRequiredMixin, UserPassesTestMixin, ListView): # New View
    model = CustomUser
    template_name = 'account/account_list.html'
    context_object_name = 'accounts'
    paginate_by = 10 # Optional: Add pagination

    def test_func(self): # Only allow staff to access this view
        return self.request.user.is_staff

    def get_queryset(self):
        # Exclude superusers from the list
        return CustomUser.objects.filter(is_superuser=False).order_by('email')

class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # New View
    model = CustomUser
    form_class = AccountUpdateForm
    template_name = 'account/account_form.html'
    context_object_name = 'account'
    success_url = reverse_lazy('account_list') # Redirect to account list after update

    def test_func(self): # Only allow staff to access this view
        return self.request.user.is_staff