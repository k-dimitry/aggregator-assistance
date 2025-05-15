from django.db import models


class Region(models.Model):
    name = models.CharField("Область", max_length=100)
    
    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'Области'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class SubRegion(models.Model):
    region = models.ForeignKey(Region, verbose_name="Регион",on_delete=models.CASCADE)
    name = models.CharField("Муниципалитеты", max_length=100)
    
    class Meta:
        verbose_name = 'Муниципалитет'
        verbose_name_plural = 'Муниципалитеты'
        ordering = ['name']
    
    def __str__(self):
        return self.name
 
class City(models.Model):
    sub_region = models.ForeignKey(SubRegion, verbose_name="Муниципалитет",on_delete=models.CASCADE)
    name = models.CharField("Город", max_length=100)
    
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']
    
    def __str__(self):
        return self.name

#district
class CityRegion(models.Model):
    city = models.ForeignKey(City, verbose_name="Город",on_delete=models.CASCADE)
    name = models.CharField("Округ", max_length=100)
    
    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Address(models.Model):
    
    city_region = models.ForeignKey(
        CityRegion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Район города",
        related_name='addresses'
    )
    street = models.CharField("Улица", max_length=100)
    house = models.CharField("Дом", max_length=20)
    apartment = models.CharField("Квартира", max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        address_parts = []
        
        if self.city_region:
            # Получаем цепочку: Region -> SubRegion -> City -> CityRegion
            region = self.city_region.city.sub_region.region.name
            sub_region = self.city_region.city.sub_region.name
            city = self.city_region.city.name
            city_region = self.city_region.name
            
            address_parts.extend([region, sub_region, city, city_region])
        
        address_parts.extend([self.street, self.house])
        
        if self.apartment:
            address_parts.append(f"кв. {self.apartment}")
        
        return ", ".join(address_parts)

class CategoryOrg(models.Model):
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("URL", max_length=100)
    desc = models.CharField("Описание", max_length=500, blank=True)
    img = models.ImageField("Изображение", upload_to=None, height_field=None, width_field=None, max_length=None, blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

class TargetGroup(models.Model):
    # class GroupType(models.TextChoices):
    #     AGE = 'age', 'Возрастная группа'
    #     SOCIAL = 'social', 'Социальная категория'
    #     HEALTH = 'health', 'Состояние здоровья'
    #     OCCUPATION = 'occupation', 'Род деятельности'

    name = models.CharField(
        "Название группы", 
        max_length=150,
        unique=True
    )
    slug = models.SlugField(
        "URL", 
        max_length=150,
        unique=True,
        help_text="Уникальное имя для URL (латиница, цифры и дефисы)"
    )
    # group_type = models.CharField(
    #     "Тип группы",
    #     max_length=20,
    #     choices=GroupType.choices,
    #     default=GroupType.SOCIAL
    # )
    description = models.TextField(
        "Описание", 
        blank=True,
        help_text="Характеристики и особенности группы"
    )
    
    icon = models.CharField(
        "Иконка", 
        max_length=50,
        blank=True,
        help_text="Класс иконки"
    )
    # age_min = models.PositiveSmallIntegerField(
    #     "Минимальный возраст", 
    #     null=True, 
    #     blank=True
    # )
    # age_max = models.PositiveSmallIntegerField(
    #     "Максимальный возраст", 
    #     null=True, 
    #     blank=True
    # )
    is_active = models.BooleanField(
        "Активна", 
        default=True,
        help_text="Отображать группу в интерфейсе"
    )
    created_at = models.DateTimeField("Созданно", auto_now_add=True)
    updated_at = models.DateTimeField("Обновленно", auto_now=True)

    class Meta:
        verbose_name = "Аудитория"
        verbose_name_plural = "Аудитории"
        ordering = ['updated_at', 'name']
        indexes = [
            models.Index(fields=['slug', 'is_active']),
        ]

    def __str__(self):
        return self.name
        # return f"{self.get_group_type_display()}: {self.name}"

    # def age_range(self):
    #     """Возвращает форматированный возрастной диапазон"""
    #     if self.age_min and self.age_max:
    #         return f"{self.age_min}-{self.age_max} лет"
    #     elif self.age_min:
    #         return f"от {self.age_min} лет"
    #     elif self.age_max:
    #         return f"до {self.age_max} лет"
    #     return "-"

class Service(models.Model):
    """Меры поддержки """
    name = models.CharField("Название", max_length=200)
    slug = models.SlugField("URL", max_length=100)
    desc = models.TextField("Описание", blank=True)
    
    target_groups = models.ManyToManyField(
        TargetGroup,
        verbose_name="Аудитории",
        related_name="services",
        help_text="Аудитории, для которых доступна эта мера"
    )
    
    organization = models.ManyToManyField(
        'Organization',
        verbose_name="Организации",
        related_name="services",
        help_text="Организации, которые оказывают меру"
    )
    
    legal = models.CharField("Закон", max_length=500)
    url_legal = models.SlugField("Ссылка на закон", max_length=500)
    requirement = models.TextField("Условия получения", max_length=2000, blank=True)
    is_free = models.BooleanField("Бесплатно")
    is_online_available = models.BooleanField("Доступно онлайн")
    # documents = models.ForeignKey(Document, verbose_name="Документы", on_delete=models.CASCADE)

    is_active = models.BooleanField(
        "Активна", 
        default=True,
        help_text="Отображать меру в интерфейсе"
    )

    class Meta:
        verbose_name = 'Мера поддержки'
        verbose_name_plural = 'Меры поддержки'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Organization(models.Model):
    ORGANIZATION_TYPES = (
        ("GOV", "Государственная"),
        ("COMM", "Коммерческая"),
        ("NPO", "НКО"),
    )

    name = models.CharField("Название", max_length=200)
    slug = models.SlugField("URL", unique=True)
    org_type = models.CharField("Тип", max_length=20, choices=ORGANIZATION_TYPES)
    description = models.TextField("Описание", blank=True)
    
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    logo = models.ImageField(
        "Логотип",
        upload_to='logos/',
        blank=True,
        null=True
    )
    
    category_org = models.ForeignKey(
        CategoryOrg, 
        verbose_name="Категория", 
        on_delete=models.CASCADE
    )

    address = models.ManyToManyField(
        Address, 
        through='OrganizationAddress',  # Указываем промежуточную модель
        verbose_name="Адрес",
        blank=True
    )
    
    is_active = models.BooleanField(
        "Активно", 
        default=True,
        help_text="Отображать организацию в интерфейсе"
    )
    
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['name']

    def __str__(self):
        return self.name

class OrganizationAddress(models.Model):
    organization = models.ForeignKey(Organization, verbose_name="Организация",on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name="Адрес",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Созданно",)  # Опционально

    class Meta:
        unique_together = ('organization', 'address')  # Запрет дублирования
        verbose_name = "Связь организации с адресом"
        verbose_name_plural = "Связи организаций с адресами"

    def __str__(self):
        return (
            f"{self.organization.name} → {self.address} "
            f"(добавлен {self.created_at.strftime('%Y-%m-%d')})"
        )

class ContactInfo(models.Model):
    """Универсальная модель контактной информации"""
    class ContactType(models.TextChoices):
        PHONE = 'phone', 'Телефон'
        EMAIL = 'email', 'Email'
        WEBSITE = 'website', 'Сайт'

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name="Организация",
    )
    contact_type = models.CharField(
        'Тип контакта',
        max_length=20,
        choices=ContactType.choices
    )
    value = models.CharField('Значение', max_length=255)
    description = models.TextField('Описание', blank=True)
    is_primary = models.BooleanField('Основной контакт', default=False)
    priority = models.PositiveIntegerField('Приоритет', default=0)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['-is_primary', 'priority']

    def __str__(self):
        return f"{self.get_contact_type_display()}: {self.value}"
    
    def get_icon(self):
        icons = {
            'phone': 'telephone',
            'email': 'envelope',
            'website': 'globe',
        }
        return icons.get(self.contact_type, 'info-circle')

class WorkingSchedule(models.Model):
    """Детализированный график работы"""
    class DayOfWeek(models.IntegerChoices):
        MONDAY = 0, 'Понедельник'
        TUESDAY = 1, 'Вторник'
        WEDNESDAY = 2, 'Среда'
        THURSDAY = 3, 'Четверг'
        FRIDAY = 4, 'Пятница'
        SATURDAY = 5, 'Суббота'
        SUNDAY = 6, 'Воскресенье'

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='working_schedules',
        verbose_name="Организация",
    )
    day_of_week = models.IntegerField(
        choices=DayOfWeek.choices,
        editable=False,
        null=False,  
        blank=False,
        verbose_name="День недели"
    )

    opens_at = models.TimeField('Открытие', null=True, blank=True)
    closes_at = models.TimeField('Закрытие', null=True, blank=True)
    is_round_the_clock = models.BooleanField('Круглосуточно', default=False)
    is_closed = models.BooleanField('Выходной', default=False)
    comment = models.CharField('Комментарий', max_length=100, blank=True)

    class Meta:
        unique_together = ('organization', 'day_of_week')
        ordering = ['day_of_week']
        verbose_name = 'График работы'
        verbose_name_plural = 'Графики работы'

    def __str__(self):
        if self.is_closed:
            return f"{self.get_day_of_week_display()}: Выходной"
        if self.is_round_the_clock:
            return f"{self.get_day_of_week_display()}: Круглосуточно"
        if self.opens_at and self.closes_at:
            return f"{self.get_day_of_week_display()}: {self.opens_at.strftime('%H:%M')} - {self.closes_at.strftime('%H:%M')}"
        return self.get_day_of_week_display()
    
    # def __str__(self):
    #     return self.get_day_of_week_display()

    # def __str__(self):
    #     if self.is_closed:
    #         return f"{self.get_day_of_week_display()}: {'Выходной'}"
    #     if self.is_round_the_clock:
    #         return f"{self.get_day_of_week_display()}: {'Круглосуточно'}"
    #     return f"{self.get_day_of_week_display()}: {self.opens_at} - {self.closes_at}"

class GeoLocation(models.Model):
    """Геолокация организации"""
    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        related_name='geo_location',
        verbose_name="Геолокация",
    )
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')

    class Meta:
        verbose_name = 'Геолокация'
        verbose_name_plural = 'Геолокации'
        
class SocialMediaProfile(models.Model):
    """Профили в социальных сетях"""
    class Platform(models.TextChoices):
        VK = 'vk', 'VKontakte'
        FB = 'fb', 'Facebook'
        INSTAGRAM = 'ig', 'Instagram'
        TELEGRAM = 'tg', 'Telegram'
        YOUTUBE = 'yt', 'YouTube'
        OTHER = 'oth', 'Другое'

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='social_profiles',
        verbose_name="Организация",
    )
    platform = models.CharField(
        'Платформа',
        max_length=3,
        choices=Platform.choices
    )
    profile_url = models.URLField('Ссылка на профиль')
    followers = models.PositiveIntegerField('Подписчики', default=0)
    is_verified = models.BooleanField('Верифицирован', default=False)

    class Meta:
        verbose_name = 'Соцсеть'
        verbose_name_plural = 'Соцсети'

    def __str__(self):
        return f"{self.get_platform_display()}: {self.profile_url}"

class OrganizationProgram(models.Model):
    """Программы и мероприятия организаций"""
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='programs',
        verbose_name="Организация",
    )
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    start_date = models.DateField('Дата начала', null=True, blank=True)
    end_date = models.DateField('Дата окончания', null=True, blank=True)
    target_groups = models.ManyToManyField(
        TargetGroup,
        blank=True,
        verbose_name="Аудитория",
    )
    is_free = models.BooleanField('Бесплатно', default=True)
    participation_conditions = models.TextField('Условия участия', blank=True)

    class Meta:
        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} ({self.organization})"