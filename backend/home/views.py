from django.shortcuts import render
from organizations.models import *
from django.db.models import Count
from .models import HeroSection, CustomSection


def index(request):
    target_groups = TargetGroup.objects.annotate(service_count=Count('services')).filter(is_active=True)

    context = {
        'herosection': HeroSection.objects.filter(is_active=True).first(),
        'custom_sections': CustomSection.objects.filter(is_active=True),
        'target_groups': target_groups,
        'total_organizations': Organization.objects.filter(is_active=True).count(),
        'total_services': Service.objects.filter(is_active=True).count()
    }
    return render(request, 'index.html', context)
