# forms.py
from dal import autocomplete
from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        widgets = {
            'city_region': autocomplete.ModelSelect2(
                url='city_region-autocomplete',
                forward=['city']
            ),
            'city': autocomplete.ModelSelect2(
                url='city-autocomplete',
                forward=['sub_region']
            ),
            'sub_region': autocomplete.ModelSelect2(
                url='sub_region-autocomplete',
                forward=['region']
            )
        }

