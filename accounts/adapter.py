from allauth.account.adapter import DefaultAccountAdapter
from accounts.allauth_forms import CustomSignupForm # Import our custom form

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_signup_form_class(self):
        return CustomSignupForm
