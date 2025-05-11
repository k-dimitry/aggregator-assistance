from django.db import models
from audience.models import SubAudience
from organizations.models import Organization


class Event(models.Model):
    name = models.CharField("Название", max_length=200)
    slug = models.SlugField("URL", unique=True)
    desc = models.TextField("Описание", blank=True)
    requirement = models.TextField("Условия", max_length=2000, blank=True)
    date_start = models.DateTimeField("Начало")
    date_end = models.DateTimeField("Окончание")
    is_free = models.BooleanField("Бесплатно")
    location = models.TextField("Место проведения", blank=True)
    registration_link = models.URLField("Ссылка на регистрацию", blank=True)
    
    """Связи"""
    organizer = models.ManyToManyField(Organization, verbose_name="Организация")
    audience = models.ManyToManyField(SubAudience, verbose_name="Аудитория")
    
    def __str__(self):
        return self.name


