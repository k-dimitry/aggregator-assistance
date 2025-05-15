from dal import autocomplete
from django import forms
from .models import *
# import django_bootstrap5

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            'name', 
            'org_type', 
            'description', 
            'logo', 
            'category_org', 
            # 'target_groups'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        # exclude = ['organization'] # form bootsrap
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
            ),
            'street': forms.TextInput(attrs={'placeholder': 'Улица'}),
            'house': forms.TextInput(attrs={'placeholder': 'Дом'}),
            'apartment': forms.TextInput(attrs={'placeholder': 'Квартира'}),
        }

class OrganizationAddressForm(forms.ModelForm):
    class Meta:
        model = OrganizationAddress
        fields = ('address',)