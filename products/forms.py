from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Only for new instances
            self.fields['prayer_text'].initial = '祈福安康'
        # Configure prayer_text field
        self.fields['prayer_text'].widget = forms.TextInput(attrs={
            'placeholder': '請輸入祈福語（最多12字）',
            'maxlength': '12'
        })
        self.fields['prayer_text'].max_length = 12

    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'prayer_text', 'description', 'is_available']
