"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from dal import autocomplete

from organizations.models import CityRegion, City, SubRegion

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Автозаполнение для CityRegion
    path(
        'city_region-autocomplete/',
        autocomplete.Select2QuerySetView.as_view(model=CityRegion),
        name='city_region-autocomplete'
    ),
    
    # Автозаполнение для City
    path(
        'city-autocomplete/',
        autocomplete.Select2QuerySetView.as_view(model=City),
        name='city-autocomplete'
    ),
    
    # Автозаполнение для SubRegion
    path(
        'sub_region-autocomplete/',
        autocomplete.Select2QuerySetView.as_view(model=SubRegion),
        name='sub_region-autocomplete'
    ),
]
