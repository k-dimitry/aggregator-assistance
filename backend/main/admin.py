from django.contrib import admin
from django.utils.html import format_html

from .models import *

from assistance.models import Assistance
from audience.models import Audience
from audience.models import SubAudience
from events.models import Event
from servises.models import Servis
from organizations.models import Organization , Address, Region, SubRegion, City, CityRegion
from organizations.forms import AddressForm

@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ('title', )
    # list_editable = ('is_active', 'order')

@admin.register(HomePageStatistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('title', 'value',)
    readonly_fields = ('value',)

class AssistanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'support_period', 'documents', 'lawful',)

class SubAudienceAdmin(admin.ModelAdmin):
    list_display = ('name', 'audience')
    
class AudienceAdmin(admin.ModelAdmin):
    list_display = ('name', )

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'date_start', 'date_end')
    
class ServisAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'requirement', 'is_free', 'documents', )

# class OrganizationAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug', 'org_type', 'address', )

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_addresses', 'org_type', 'update_date')
    
    def display_addresses(self, obj):
        # Получаем все адреса организации
        addresses = obj.address.all()
        # Формируем HTML-список адресов
        address_list = [
            f"<li>{address}</li>" 
            for address in addresses
        ]
        return format_html("<ul>{}</ul>", "".join(address_list)) if address_list else "-"
    
    display_addresses.short_description = "Адрес"

class AddressAdmin(admin.ModelAdmin):
    form = AddressForm
    
    list_display = ('__str__', 'region', 'sub_region', 'city', 'city_region')
    
    @admin.display(description="Регион")
    def region(self, obj):
        return obj.city_region.city.sub_region.region if obj.city_region else None

    @admin.display(description="Субрегион")
    def sub_region(self, obj):
        return obj.city_region.city.sub_region if obj.city_region else None

    @admin.display(description="Город")
    def city(self, obj):
        return obj.city_region.city if obj.city_region else None

admin.site.register(Address, AddressAdmin)

admin.site.register(Servis, ServisAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Audience, AudienceAdmin)
admin.site.register(SubAudience, SubAudienceAdmin)
admin.site.register(Assistance, AssistanceAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register([Region, SubRegion, City, CityRegion])