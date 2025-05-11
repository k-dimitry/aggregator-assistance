from django.db import models


class Audience(models.Model):
    """Целевые группы (для кого предназначены услуги)"""

    name = models.CharField("Целевая группа", max_length=200)
    desc = models.TextField("Описание", max_length=2000, blank=True)
    #icon_group = models.ImageField("Иконка", upload_to=None, height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return self.name


class SubAudience(models.Model):
    """Целевые группы (для кого предназначены услуги)"""

    audience = models.ForeignKey(Audience, on_delete=models.CASCADE)
    name = models.CharField("Подгруппа", max_length=200)
    desc = models.TextField("Описание", max_length=2000, blank=True)
    # requirement = models.TextField("Условия", max_length=4000)
    #icon_group = models.ImageField("Иконка", upload_to=None, height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return self.name