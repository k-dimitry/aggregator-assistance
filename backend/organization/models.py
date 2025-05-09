from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey

class Organization(models.Model):
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    # address =

    description = models.TextField()

    
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['publish']
        indexes = [models.Index(fields=['-publish'])]

    def __str__(self):
        return self.title