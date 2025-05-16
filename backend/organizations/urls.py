from django.urls import path

from .views import *


urlpatterns = [
    path('', OrganizationList.as_view(), name='organization_list'),
    path('<slug:slug>/', OrganizationDetailView.as_view(), name='organization_detail'),
]
