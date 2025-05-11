from django.db import models
from audience.models import SubAudience

    

class Document(models.Model):
    name = models.CharField("Название", max_length=200)
    
    def __str__(self):
        return self.name

class Lawful(models.Model):
    name = models.CharField("Название", max_length=200)
    link = models.URLField("Ссылка на закон", blank=True)
    
    def __str__(self):
        return self.name

class Assistance(models.Model):
    """Ц"""
    
    
    name = models.CharField("Название", max_length=200)
    desc = models.TextField("Описание", blank=True)
    requirement = models.TextField("Условия получения", max_length=2000, blank=True)
    
    support_period = models.DateField("Срок действия помощи")
    
    documents = models.ForeignKey(Document, verbose_name="Документы", on_delete=models.CASCADE)
    lawful = models.ForeignKey(Lawful, verbose_name="Основания", on_delete=models.CASCADE)
    
    # data_create = models.DateField("Дата публикации", auto_now=False, auto_now_add=False)
    # data_update = models.DateField("Дата обновления", auto_now=False, auto_now_add=False)
    
    """Связи"""
    audience = models.ForeignKey(SubAudience, verbose_name="Аудитория", on_delete=models.CASCADE)

    
    def __str__(self):
        return self.name
    
    
    # documents = models.TextField("Необходимые документы")
    # application_template = models.FileField("Шаблон заявления", upload_to="templates/", blank=True)


