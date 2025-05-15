from django.urls import path

from .views import *


urlpatterns = [
    path('', OrganizationList.as_view(), name='organization_list'),
    # path('new/', OrganizationCreateView.as_view(), name='organization_create'),
    path('/<slug:slug>/', OrganizationDetailView.as_view(), name='organization_detail'),
    # path('', OrganizationList.as_view(), name='home'),
]
