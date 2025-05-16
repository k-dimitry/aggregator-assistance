from django.views.generic import ListView, CreateView, DetailView, TemplateView, UpdateView
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from .models import *
from .forms import *
from django.forms import inlineformset_factory

def group_detail(request, pk):
    group = get_object_or_404(TargetGroup, pk=pk)
    services = group.services.filter(is_active=True)
    
    context = {
        'group': group,
        'services': services
    }
    return render(request, 'organizations/group_detail.html', context)


    
class OrganizationDetailView(DetailView):
    model = Organization
    template_name = 'organizations/org_detail.html'
    context_object_name = 'organization'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization = self.get_object()
        
        # Дополнительные данные при необходимости
        context['services'] = organization.services.all()
        return context    


class OrganizationList(ListView):
    model = Organization
    # template_name = "index.html"
    template_name = 'organizations/org_list.html'
    context_object_name = 'organizations'


# class OrganizationCreateView(CreateView):
#     model = Organization
#     form_class = OrganizationForm
#     template_name = "organizations/org_form.html"
#     success_url = reverse_lazy("organization_list")

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context["address_formset"] = OrganizationAddressFormSet(self.request.POST)
#         else:
#             context["address_formset"] = OrganizationAddressFormSet()
#         return context

#     def form_valid(self, form):
#         context = self.get_context_data()
#         address_formset = context["address_formset"]

#         if address_formset.is_valid():
#             self.object = form.save()
#             addresses = address_formset.save(commit=False)
#             for address in addresses:
#                 address.organization = self.object
#                 address.save()
#             return super().form_valid(form)
#         return self.render_to_response(self.get_context_data(form=form))


OrganizationAddressFormSet = inlineformset_factory(
    Organization,
    OrganizationAddress, 
    form=OrganizationAddressForm,
    fields=("address",),  
    extra=1,
    can_delete=True,
    widgets={
        'address': forms.Select(attrs={'class': 'form-select'})
    }
)
