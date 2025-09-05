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
    
    # Load address data from JSON file
    with open('static/data/CityCountyData.json', 'r', encoding='utf-8') as f:
        address_data = json.load(f)
    
    COUNTY_CHOICES = [('', '請選擇縣市')] + [(city['CityName'], city['CityName']) for city in address_data]
    DISTRICT_CHOICES = [('', '請先選擇縣市')]

    address_county = forms.ChoiceField(
        choices=COUNTY_CHOICES,
        label='縣市',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    address_district = forms.ChoiceField(
        choices=DISTRICT_CHOICES,
        label='鄉鎮市區',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = [
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
        ]
        widgets = {
            'gregorian_birth_date': forms.DateInput(attrs={'type': 'date'}),
            'gregorian_birth_time': forms.TimeInput(attrs={'type': 'time'}),
            'lunar_birth_date': forms.TextInput(attrs={'readonly': 'readonly'}),
            'lunar_birth_time': forms.TextInput(attrs={'readonly': 'readonly'}),
            'address_zip_code': forms.TextInput(attrs={'readonly': 'readonly'}),
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
            'address_county',
            'address_district',
            'address_zip_code',
            'address_detail',
            Submit('submit', '儲存個人資料')
        )
        
        # Pass the address data to the template through the form's context
        self.fields['address_county'].widget.attrs['data-address-data'] = json.dumps(self.address_data)

        # This is the new logic
        if 'address_county' in self.data:
            try:
                county_name = self.data.get('address_county')
                city_data = next((city for city in self.address_data if city['CityName'] == county_name), None)
                if city_data:
                    self.fields['address_district'].choices = [('', '請選擇鄉鎮市區')] + [
                        (area['AreaName'], area['AreaName']) for area in city_data['AreaList']
                    ]
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty choices
        elif self.instance and self.instance.address_county:
            city_name = self.instance.address_county
            city_data = next((city for city in self.address_data if city['CityName'] == city_name), None)
            if city_data:
                self.fields['address_district'].choices = [('', '請選擇鄉鎮市區')] + [
                    (area['AreaName'], area['AreaName']) for area in city_data['AreaList']
                ]

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

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'gender',
            'gregorian_birth_date',
            'gregorian_birth_time',
            'address_zip_code',
            'address_county',
            'address_district',
            'address_detail',
            'is_active',
            'is_staff',
        ]
        widgets = {
            'gregorian_birth_date': forms.DateInput(attrs={'type': 'date'}),
            'gregorian_birth_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'gender',
            'gregorian_birth_date',
            'gregorian_birth_time',
            'address_zip_code',
            'address_county',
            'address_district',
            'address_detail',
            'is_active',
            'is_staff',
            Submit('submit', '儲存帳號資料')
        )
