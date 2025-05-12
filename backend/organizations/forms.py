# forms.py
from dal import autocomplete
from django import forms
from .models import *

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            'name', 
            'org_type', 
            'description', 
            'logo', 
            'category_org', 
            'target_groups'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ['organization'] # form bootsrap
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

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['contact_type', 'value', 'is_primary']

class WorkingScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkingSchedule
        fields = ['day_of_week', 'opens_at', 'closes_at', 'is_round_the_clock', 'is_closed']