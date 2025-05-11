from django.views.generic import DetailView
from organizations.models import Organization
from servises.models import Servis

from django.db.models import Count
from .models import (
    HeroBanner,
    HomePageStatistic,
)


class OrganizationDetailView(DetailView):
    model = Organization
    template_name = 'organizations/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = self.object.services.all()
        return context
    

class HomeView(DetailView):
    template_name = 'core/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Динамический баннер
        # context['active_banners'] = HeroBanner.objects.filter(is_active=True).order_by('order')[:3]
        
        # Форма проверки соответствия
        # context['eligibility_form'] = QuickEligibilityForm()
        
        # Популярные категории (топ-5 услуг)
        context['popular_services'] = Servis.objects.annotate(
            num_orgs=Count('organization')
        ).order_by('-num_orgs')[:5]
        
        # Новые и обновленные организации
        context['new_organizations'] = Organization.objects.order_by('-update_date')[:6]
        
        # Статистика
        HomePageStatistic.update_stats()
        context['statistics'] = HomePageStatistic.objects.all()
        
        # Дополнительные блоки
        # context['latest_news'] = NewsArticle.objects.all()[:3]
        # context['partners'] = Partner.objects.all()
        # context['useful_links'] = UsefulLink.objects.all()
        # context['testimonials'] = Testimonial.objects.filter(is_approved=True)[:4]
        
        return context

    # def post(self, request, *args, **kwargs):
    #     form = QuickEligibilityForm(request.POST)
    #     if form.is_valid():
    #         # Логика обработки формы
    #         return self.eligibility_check_response(form)
    #     return self.render_to_response(self.get_context_data(form=form))