# organizations/views.py
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import *
from .forms import OrganizationForm, AddressForm, ContactInfoForm, WorkingScheduleForm
from django.forms import inlineformset_factory

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organizations/organization_form.html'
    success_url = reverse_lazy('organization_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['address_formset'] = AddressFormSet(self.request.POST)
            context['contact_formset'] = ContactFormSet(self.request.POST)
            context['schedule_formset'] = ScheduleFormSet(self.request.POST)
        else:
            context['address_formset'] = AddressFormSet()
            context['contact_formset'] = ContactFormSet()
            context['schedule_formset'] = ScheduleFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        address_formset = context['address_formset']
        contact_formset = context['contact_formset']
        schedule_formset = context['schedule_formset']
        
        if (address_formset.is_valid() and 
            contact_formset.is_valid() and 
            schedule_formset.is_valid()):
            
            self.object = form.save()
            
            address_formset.instance = self.object
            address_formset.save()
            
            contact_formset.instance = self.object
            contact_formset.save()
            
            schedule_formset.instance = self.object
            schedule_formset.save()
            
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

AddressFormSet = inlineformset_factory(
    Organization,
    Address,
    form=AddressForm,
    extra=1,
    can_delete=True
)

ContactFormSet = inlineformset_factory(
    Organization,
    ContactInfo,
    form=ContactInfoForm,
    extra=1,
    can_delete=True
)

ScheduleFormSet = inlineformset_factory(
    Organization,
    WorkingSchedule,
    form=WorkingScheduleForm,
    extra=7,
    can_delete=False
)