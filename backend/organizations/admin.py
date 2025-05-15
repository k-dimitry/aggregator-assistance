from django.contrib import admin
from django.utils.html import format_html
from .forms import AddressForm
from django.http import HttpRequest

from .models import *

# @admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']


# @admin.register(SubRegion)
class SubRegionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'region']

# @admin.register(City)
class CityAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'sub_region']

# @admin.register(CityRegion)
class CityRegionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'city']

# class AddressInline(admin.StackedInline):
#     model = Address
#     extra = 1
#     fields = (
#         ('city_region', 'city'),
#         ('sub_region', 'region'),
#         ('street', 'house', 'apartment'),
#     )
#     # autocomplete_fields = ['city_region', 'city', 'sub_region']
#     verbose_name = "Адрес"
#     verbose_name_plural = "Адреса организации"

#     def get_formset(self, request, obj=None, **kwargs):
#         formset = super().get_formset(request, obj, **kwargs)
#         formset.form.base_fields['city_region'].widget.can_add_related = False
#         formset.form.base_fields['city'].widget.can_add_related = False
#         formset.form.base_fields['sub_region'].widget.can_add_related = False
#         return formset


@admin.register(OrganizationAddress)
class OrganizationAddressAdmin(admin.ModelAdmin):
    list_display = ('organization', 'address', 'created_at')
    list_filter = ('organization', 'address')
    
# @admin.register(TargetGroup)
class TargetGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        # 'group_type',
        # 'age_range',
        'icon_preview',
        'is_active',
        'updated_at'
    )
    list_filter = (
        # 'group_type',
        'is_active',
        'created_at'
    )
    search_fields = (
        'name',
        'description',
        'slug'
    )
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'slug',
                # 'group_type',
                'is_active'
            )
        }),
        ('Описание', {
            'fields': (
                'description',
                'icon'
            ),
            'classes': ('collapse',)
        }),
        # ('Возрастные параметры', {
        #     'fields': (
        #         'age_min',
        #         'age_max'
        #     ),
            # 'classes': ('collapse',)
        # }),
        ('Даты', {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )

    # @admin.display(description='Возрастной диапазон')
    # def age_range(self, obj):
    #     return obj.age_range()

    @admin.display(description='Иконка')
    def icon_preview(self, obj):
        if obj.icon:
            return format_html(f'<i class="bi {obj.icon} fs-4"></i>')
        return '-'

class ContactInfoInline(admin.TabularInline):
    model = ContactInfo
    extra = 1  # Количество пустых форм для добавления
    fields = ("contact_type", "value", "is_primary", "priority")
    ordering = ("-is_primary", "priority")

class GeoLocationInline(admin.StackedInline):
    model = GeoLocation
    extra = 1
    fields = ("latitude", "longitude")


class SocialMediaProfileInline(admin.TabularInline):
    model = SocialMediaProfile
    extra = 1
    fields = ("platform", "profile_url", "is_verified")

class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = [
        "name",
        "is_free",
        "desc",
        'legal'
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

# class WorkingSchedule(admin.ModelAdmin):
#     list_display = ("organization",)

class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("organization", "value", "is_primary")

class CategoryOrgAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = (
        "name",
        "slug",
    )

class OrganizationAddressInline(admin.TabularInline):
    model = OrganizationAddress
    extra = 1  # Количество пустых форм для добавления новых адресов
    autocomplete_fields = ['address']
    verbose_name = "Связанный адрес"
    verbose_name_plural = "Связанные адреса"
    # Опционально: фильтрация существующих адресов
    # raw_id_fields = ('address',)  # Покажет поисковую форму вместо выпадающего списка

# class OrganizationServiceInline(admin.TabularInline):
#     model = OrganizationService
#     extra = 1
#     autocomplete_fields = ["service"]
#     fields = ("service", "is_main_service", "duration")
    
#     # Дополнительные настройки (опционально)
#     # fields = ('service', 'price', 'price_type', 'is_main_service')
#     # show_change_link = True

@admin.register(WorkingSchedule)
class WorkingScheduleAdmin(admin.ModelAdmin):
    list_display = ('organization', 'day_of_week', 'is_closed', 'is_round_the_clock')
    list_filter = ('organization', 'day_of_week', 'is_closed', 'is_round_the_clock')

class WorkingScheduleInline(admin.TabularInline):
    model = WorkingSchedule
    extra = 0
    max_num = 7
    can_delete = False
    readonly_fields = ('day_of_week_display', 'schedule_summary')
    fields = (
        'day_of_week_display',
        'schedule_summary',
        'opens_at',
        'closes_at',
        'is_round_the_clock',
        'is_closed',
        'comment'
    )

    def day_of_week_display(self, obj):
        return obj.get_day_of_week_display()
    day_of_week_display.short_description = 'День недели'

    def schedule_summary(self, obj):
        if obj.is_closed:
            return format_html('<span style="color: red; font-weight: bold;">Выходной</span>')
        if obj.is_round_the_clock:
            return format_html('<span style="color: green; font-weight: bold;">Круглосуточно</span>')
        if obj.opens_at and obj.closes_at:
            return format_html('{} - {}', obj.opens_at.strftime('%H:%M'), obj.closes_at.strftime('%H:%M'))
        return '-'
    schedule_summary.short_description = 'График'

    def has_add_permission(self, request, obj=None):
        return False

class OrganizationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = (
        "name",
        "display_addresses",
        "org_type",
    )
    inlines = [
        # AddressInline,
        OrganizationAddressInline,
        GeoLocationInline,
        # OrganizationServiceInline,
        ContactInfoInline,
        SocialMediaProfileInline,
        WorkingScheduleInline,
        
    ]

    # Для ManyToMany-полей используйте фильтры
    # filter_horizontal = ('categories', 'services', 'target_groups')
    # filter_horizontal = ['name', 'target_groups']
    # Основные поля
    fieldsets = (
        (None, {"fields": ("name", "slug", 'org_type', "description", "logo", "category_org")}),
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
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Создаем записи для всех дней недели при создании организации
        if not change:
            for day in WorkingSchedule.DayOfWeek:  # Используем Enum-значения
                WorkingSchedule.objects.get_or_create(
                    organization=obj,
                    day_of_week=day.value,  # Явно задаем значение
                    defaults={
                        'opens_at': None,
                        'closes_at': None,
                        'is_round_the_clock': False,
                        'is_closed': False
                    }
                )

class AddressAdmin(admin.ModelAdmin):
    form = AddressForm
    search_fields = [
        'street', 
        'house',
        'city__name',
        'sub_region__name',
        'region__name'
    ]

    list_display = ("__str__", "city", "city_region", 'street')
    list_filter = ( 'city_region', 'street')

    @admin.display(description="Регион")
    def region(self, obj):
        return obj.city_region.city.sub_region.region if obj.city_region else None

    @admin.display(description="Субрегион")
    def sub_region(self, obj):
        return obj.city_region.city.sub_region if obj.city_region else None

    @admin.display(description="Город")
    def city(self, obj):
        return obj.city_region.city if obj.city_region else None

    
admin.site.register(TargetGroup, TargetGroupAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(OrganizationProgram, OrganizationProgramAdmin)
# admin.site.register(SocialMediaProfile, SocialMediaProfileAdmin)
# admin.site.register(GeoLocation, GeoLocationAdmin)
# admin.site.register(WorkingSchedule)
# admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(CategoryOrg, CategoryOrgAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register([Region, SubRegion, City, CityRegion])
