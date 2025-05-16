from django.urls import path

from .views import *
from . import views



urlpatterns = [
    path('', OrganizationList.as_view(), name='organization_list'),
    path('<slug:slug>/', OrganizationDetailView.as_view(), name='organization_detail'),
    path('group/<int:pk>/', views.group_detail, name='group-detail'),
]
