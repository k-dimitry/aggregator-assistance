from django.contrib import admin
from django.utils.html import format_html
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import *


class ServiceAdminForm(forms.ModelForm):
    desc = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Service
        fields = '__all__'
        
class OrganizationAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание',widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Organization
        fields = '__all__'

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False  

@admin.register(SubRegion)
class SubRegionAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False 

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False 

@admin.register(CityRegion)
class CityRegionAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False  

@admin.register(WorkingSchedule)
class WorkingScheduleAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False  

@admin.register(OrganizationAddress)
class OrganizationAddressAdmin(admin.ModelAdmin):
    list_display = ('organization', 'address', 'created_at')
    list_filter = ('organization', 'address')
    
@admin.register(TargetGroup)
class TargetGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'icon_preview',
        'is_active',
        'updated_at'
    )
    list_filter = (
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

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    form = ServiceAdminForm
    filter_horizontal = ['target_groups', 'organization']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = [
        "name",
        "is_free",
        "desc",
        'legal'
    ]
    list_display = ("name", "is_free", "is_online_available")
    list_filter = ("is_free", "is_online_available")

@admin.register(OrganizationProgram)
class OrganizationProgramAdmin(admin.ModelAdmin):
    list_display = ("organization", "name", "start_date", "end_date", "is_free")

@admin.register(CategoryOrg)
class CategoryOrgAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = (
        "name",
        "slug",
    )

class GeoLocationAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "latitude",
        "longitude",
    )

class GeoLocationInline(admin.StackedInline):
    model = GeoLocation
    extra = 1
    classes = ["collapse"]
    fields = ("latitude", "longitude")

class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("organization", "value", "is_primary")

class ContactInfoInline(admin.TabularInline):
    model = ContactInfo
    extra = 1 
    classes = ["collapse"]
    fields = ("contact_type", "value", "is_primary", "priority")
    ordering = ("-is_primary", "priority")

class SocialMediaProfileAdmin(admin.ModelAdmin):
    list_display = ("organization",)

class SocialMediaProfileInline(admin.TabularInline):
    model = SocialMediaProfile
    extra = 1
    classes = ["collapse"]
    fields = ("platform", "profile_url", "is_verified")

class OrganizationAddressInline(admin.TabularInline):
    model = OrganizationAddress
    extra = 1  
    autocomplete_fields = ['address']
    classes = ["collapse"]
    verbose_name = "Связанный адрес"
    verbose_name_plural = "Связанные адреса"

class WorkingScheduleInline(admin.TabularInline):
    model = WorkingSchedule
    extra = 0
    classes = ["collapse"]
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

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    search_fields = [
        'street', 
        'house',
        'city__name',
        'sub_region__name',
        'region__name'
    ]
    
    # filter_horizontal = ('region', 'sub_region', 'city', 'city_region')
    # raw_id_fields = ('region', 'sub_region', 'city', 'city_region')
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

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    form = OrganizationAdminForm
    prepopulated_fields = {'slug': ('name',)}
    list_display = (
        "name",
        "display_addresses",
        "org_type",
    )
    inlines = [
        OrganizationAddressInline,
        GeoLocationInline,
        ContactInfoInline,
        SocialMediaProfileInline,
        WorkingScheduleInline,
        
    ]

    fieldsets = (
        (None, {
            "fields": (
                "name", 
                "slug", 
                'org_type', 
                "description", 
                "logo", 
                "category_org"
            ),
        }),      
    )

    def display_addresses(self, obj):
        addresses = obj.address.all()
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

