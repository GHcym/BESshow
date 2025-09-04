import json # New import
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from .models import CustomUser
from allauth.account.forms import SignupForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .utils import convert_gregorian_to_lunar

class CustomUserCreationForm(AdminUserCreationForm):

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
        )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = "__all__"

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'gender',
            'gregorian_birth_date',
            'gregorian_birth_time',
            'lunar_birth_date', # Keep in fields for model saving
            'lunar_birth_time', # Keep in fields for model saving
            'phone_number',
            'address_zip_code',
            'address_county',
            'address_district',
            'address_detail',
        ]
        widgets = {
            'gregorian_birth_date': forms.DateInput(attrs={'type': 'date'}),
            'gregorian_birth_time': forms.TimeInput(attrs={'type': 'time'}),
            'lunar_birth_date': forms.TextInput(attrs={'readonly': 'readonly'}), # Make read-only
            'lunar_birth_time': forms.TextInput(attrs={'readonly': 'readonly'}), # Make read-only
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'first_name',
            'gender',
            'gregorian_birth_date',
            'gregorian_birth_time',
            'lunar_birth_date',
            'lunar_birth_time',
            'phone_number',
            'address_zip_code',
            'address_county',
            'address_district',
            'address_detail',
            Submit('submit', '儲存個人資料')
        )

    def clean(self):
        cleaned_data = super().clean()
        gregorian_birth_date = cleaned_data.get('gregorian_birth_date')
        gregorian_birth_time = cleaned_data.get('gregorian_birth_time')

        if gregorian_birth_date:
            lunar_date_str, lunar_time_str = convert_gregorian_to_lunar(
                gregorian_birth_date, gregorian_birth_time
            )
            cleaned_data['lunar_birth_date'] = lunar_date_str
            cleaned_data['lunar_birth_time'] = lunar_time_str
        else:
            # If Gregorian birth date is not provided, clear lunar fields
            cleaned_data['lunar_birth_date'] = ""
            cleaned_data['lunar_birth_time'] = ""

        return cleaned_data

