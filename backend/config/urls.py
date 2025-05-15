
from django.contrib import admin
from django.urls import path, include
from dal import autocomplete
from django.conf import settings
from django.conf.urls.static import static
# from organizations.views import Test
from organizations.models import CityRegion, City, SubRegion
from home.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    
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
    
    
    path( '', include('home.urls')),
    path( 'orgatnizations/', include('organizations.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)