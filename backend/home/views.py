from django.shortcuts import render

from .models import HeroSection, CustomSection

def index(request):
    context = {
        'herosection': HeroSection.objects.filter(is_active=True).first(),
        'custom_sections': CustomSection.objects.filter(is_active=True)
    }
    return render(request, 'index.html', context)