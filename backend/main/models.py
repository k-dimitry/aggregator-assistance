from django.db import models
from assistance.models import Assistance
from audience.models import SubAudience
from events.models import Event
from organizations.models import Organization
from servises.models import Servis


class HeroBanner(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    subtitle = models.TextField("Подзаголовок")
    button_text = models.CharField("Текст кнопки", max_length=50, default="Начать проверку")
    # button_link = models.CharField("Ссылка кнопки", max_length=100, default="/check-eligibility")
    # background_image = models.ImageField("Фоновое изображение", upload_to='banners/')
    # is_active = models.BooleanField("Активный баннер", default=True)
    # order = models.PositiveIntegerField("Порядок отображения", default=0)

    # class Meta:
    #     ordering = ['order']

# class QuickEligibilityQuestion(models.Model):
#     QUESTION_TYPES = (
#         ('SINGLE', 'Один ответ'),
#         ('MULTI', 'Несколько ответов'),
#     )
    
#     text = models.CharField("Вопрос", max_length=255)
#     help_text = models.TextField("Подсказка", blank=True)
#     question_type = models.CharField("Тип вопроса", max_length=20, choices=QUESTION_TYPES, default='SINGLE')
#     priority = models.IntegerField("Приоритет", default=0)

#     def __str__(self):
#         return self.text

class HomePageStatistic(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    value = models.IntegerField("Значение")
    # icon = models.CharField("Иконка", max_length=50, help_text="Класс иконки (например, fa-users)")
    
    @classmethod
    def update_stats(cls):
        """Автоматическое обновление статистики"""
        orgs_count, _ = cls.objects.get_or_create(title="Организаций в базе")
        orgs_count.value = Organization.objects.count()
        orgs_count.save()
        
        services_count, _ = cls.objects.get_or_create(title="Доступных услуг")
        services_count.value = Servis.objects.count()
        services_count.save()

# class NewsArticle(models.Model):
#     title = models.CharField("Заголовок", max_length=200)
#     excerpt = models.TextField("Краткое содержание", max_length=300)
#     pub_date = models.DateField("Дата публикации", auto_now_add=True)
#     link = models.URLField("Ссылка на новость")

#     class Meta:
#         ordering = ['-pub_date']

# class Partner(models.Model):
#     name = models.CharField("Название", max_length=100)
#     logo = models.ImageField("Логотип", upload_to='partners/')
#     website = models.URLField("Сайт партнера")

# class UsefulLink(models.Model):
#     title = models.CharField("Название", max_length=100)
#     url = models.URLField("Ссылка")
#     category = models.CharField("Категория", max_length=50)