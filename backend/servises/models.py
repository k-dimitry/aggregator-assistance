from django.db import models
from audience.models import SubAudience

class Document(models.Model):
    name = models.CharField("Название", max_length=200)
    
    def __str__(self):
        return self.name

class Servis(models.Model):
    """Ц"""
    name = models.CharField("Название", max_length=200)
    desc = models.TextField("Описание", blank=True)
    
    requirement = models.TextField("Условия получения", max_length=2000, blank=True)
    is_free = models.BooleanField("Бесплатно")
    documents = models.ForeignKey(Document, verbose_name="Документы", on_delete=models.CASCADE)
    
    """Связи"""
    audience = models.ForeignKey(SubAudience, verbose_name="Аудитория", on_delete=models.CASCADE)

    
    def __str__(self):
        return self.name
    

