from django.contrib import admin
from django import forms
from django.contrib import admin
from .models import HeroSection, CustomSection
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class CustomSectionAdminForm(forms.ModelForm):
    html_content = forms.CharField(widget=CKEditorUploadingWidget())
    
    class Meta:
        model = CustomSection
        fields = '__all__'


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'image_preview', 'created_at')
    list_editable = ('is_active',)
    readonly_fields = ('image_preview',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'button_text')
        }),
        ('Изображение', {
            'fields': ('background_image', 'image_preview')
        }),
        ('Статус', {
            'fields': ('is_active',)
        })
    )

@admin.register(CustomSection)
class CustomSectionAdmin(admin.ModelAdmin):
    form = CustomSectionAdminForm
    list_display = ('name', 'is_active', 'created_at')
    list_editable = ('is_active',)
    search_fields = ('name', 'html_content')
    fieldsets = (
        (None, {
            'fields': ('name', 'html_content', 'is_active')
        }),
    )
    actions = ['activate_sections', 'deactivate_sections']

    def activate_sections(self, request, queryset):
        queryset.update(is_active=True)
    activate_sections.short_description = "Активировать выбранные секции"

    def deactivate_sections(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_sections.short_description = "Деактивировать выбранные секции"