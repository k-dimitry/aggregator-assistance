from django.db import models

from django.db import models
from django.utils.safestring import mark_safe

class HeroSection(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')
    button_text = models.CharField('Текст кнопки', max_length=50)
    background_image = models.ImageField(
        'Фоновое изображение',
        upload_to='hero/'
    )
    is_active = models.BooleanField('Активный', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Секция Hero'
        verbose_name_plural = 'Секция Hero'

    def __str__(self):
        return self.title

    def image_preview(self):
        if self.background_image:
            return mark_safe(f'<img src="{self.background_image.url}" width="200" />')
        return "Нет изображения"
    image_preview.short_description = 'Превью'

class CustomSection(models.Model):
    name = models.CharField('Название секции', max_length=100, unique=True)
    html_content = models.TextField('HTML содержимое')
    is_active = models.BooleanField('Активная', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Кастомная секция'
        verbose_name_plural = 'Кастомные секции'

    def __str__(self):
        return self.name