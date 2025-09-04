from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from allauth.account.forms import SignupForm as AllauthSignupForm # Renamed to avoid confusion

class CustomSignupForm(AllauthSignupForm): # Inherit from AllauthSignupForm directly
    first_name = forms.CharField(max_length=50, label="First Name", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Removed diagnostic prints
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            'first_name', # Include the new field
            'password1',  # Use 'password1' as it's the actual field name
            Submit('submit', 'Sign up')
        )

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.save()
        return user