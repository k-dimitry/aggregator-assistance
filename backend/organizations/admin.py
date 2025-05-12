from django.contrib import admin
from django.utils.html import format_html
from .forms import AddressForm

from .models import *


class ContactInfoInline(admin.TabularInline):
    model = ContactInfo
    extra = 1  # Количество пустых форм для добавления
    fields = ("contact_type", "value", "is_primary", "priority")
    ordering = ("-is_primary", "priority")


class GeoLocationInline(admin.StackedInline):
    model = GeoLocation
    extra = 1
    fields = ("latitude", "longitude")


class WorkingScheduleInline(admin.TabularInline):
    model = WorkingSchedule
    extra = 7  # По одному на каждый день недели
    fields = (
        "day_of_week",
        "opens_at",
        "closes_at",
        "is_round_the_clock",
        "is_closed",
        "comment",
    )


class SocialMediaProfileInline(admin.TabularInline):
    model = SocialMediaProfile
    extra = 1
    fields = ("platform", "profile_url", "is_verified")


class ServiceAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
        "is_free",
        "desc",
    ]
    list_display = ("name", "is_free", "is_online_available")
    list_filter = ("is_free", "is_online_available")


class OrganizationProgramAdmin(admin.ModelAdmin):
    list_display = ("organization", "name", "start_date", "end_date", "is_free")


class SocialMediaProfileAdmin(admin.ModelAdmin):
    list_display = ("organization",)


class GeoLocationAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "latitude",
        "longitude",
    )


class WorkingSchedule(admin.ModelAdmin):
    list_display = ("organization",)


class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("organization", "value", "is_primary")


class CategoryOrgAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )


class OrganizationAddressInline(admin.TabularInline):
    model = OrganizationAddress
    extra = 1  # Количество пустых форм для добавления новых адресов
    # Опционально: фильтрация существующих адресов
    # raw_id_fields = ('address',)  # Покажет поисковую форму вместо выпадающего списка


class OrganizationServiceInline(admin.TabularInline):
    model = OrganizationService
    extra = 1
    autocomplete_fields = ["service"]
    fields = ("service", "is_main_service", "duration")
    
    # Дополнительные настройки (опционально)
    # fields = ('service', 'price', 'price_type', 'is_main_service')
    # show_change_link = True


class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "display_addresses",
        "org_type",
    )
    inlines = [
        OrganizationServiceInline,
        OrganizationAddressInline,
        GeoLocationInline,
        ContactInfoInline,
        WorkingScheduleInline,
        SocialMediaProfileInline,
    ]

    # Для ManyToMany-полей используйте фильтры
    # filter_horizontal = ('categories', 'services', 'target_groups')
    # filter_horizontal = ['name', 'target_groups']
    # Основные поля
    fieldsets = (
        (None, {"fields": ("name", "slug", "description", "logo")}),
        (
            "Классификация",
            {"fields": ("category_org", "target_groups"), "classes": ("collapse",)},
        ),
    )

    def display_addresses(self, obj):
        # Получаем все адреса организации
        addresses = obj.address.all()
        # Формируем HTML-список адресов
        address_list = [f"{address}" for address in addresses]
        return (
            format_html("<ul>{}</ul>", "".join(address_list)) if address_list else "-"
        )

    display_addresses.short_description = "Адрес"


class AddressAdmin(admin.ModelAdmin):
    form = AddressForm

    list_display = ("__str__", "region", "sub_region", "city", "city_region")

    @admin.display(description="Регион")
    def region(self, obj):
        return obj.city_region.city.sub_region.region if obj.city_region else None

    @admin.display(description="Субрегион")
    def sub_region(self, obj):
        return obj.city_region.city.sub_region if obj.city_region else None

    @admin.display(description="Город")
    def city(self, obj):
        return obj.city_region.city if obj.city_region else None


admin.site.register(Service, ServiceAdmin)
admin.site.register(OrganizationProgram, OrganizationProgramAdmin)
admin.site.register(SocialMediaProfile, SocialMediaProfileAdmin)
admin.site.register(GeoLocation, GeoLocationAdmin)
# admin.site.register(WorkingSchedule)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(CategoryOrg, CategoryOrgAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register([Region, SubRegion, City, CityRegion])
