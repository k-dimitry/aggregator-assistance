from django.db import models

class CategoryOrg(models.Model):
    name = models.CharField("", max_length=100)
    slug = models.SlugField("URL", max_length=100)
    desc = models.CharField("", max_length=500, blank=True)
    img = models.ImageField("", upload_to=None, height_field=None, width_field=None, max_length=None, blank=True, null=True)

    def __str__(self):
        return self.name

class TargetGroup(models.Model):
    pass

class Service(models.Model):
    """Ц"""
    name = models.CharField("Название", max_length=200)
    desc = models.TextField("Описание", blank=True)
    
    requirement = models.TextField("Условия получения", max_length=2000, blank=True)
    is_free = models.BooleanField("Бесплатно")
    is_online_available = models.BooleanField("is online available")
    # documents = models.ForeignKey(Document, verbose_name="Документы", on_delete=models.CASCADE)
    
    """Связи"""
    audience = models.ForeignKey(TargetGroup, verbose_name="Аудитория", on_delete=models.CASCADE)

    
    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField("Область", max_length=100)
    
    def __str__(self):
        return self.name

class SubRegion(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField("Муниципалитеты", max_length=100)
    
    def __str__(self):
        return self.name
 
class City(models.Model):
    sub_region = models.ForeignKey(SubRegion, on_delete=models.CASCADE)
    name = models.CharField("Город", max_length=100)
    
    def __str__(self):
        return self.name

#district
class CityRegion(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField("Округ", max_length=100)
    
    def __str__(self):
        return self.name

class Address(models.Model):
    city_region = models.ForeignKey(CityRegion, on_delete=models.SET_NULL, null=True)
    street = models.CharField("Улица", max_length=100)
    house = models.CharField("Дом", max_length=20)
    apartment = models.CharField("Квартира", max_length=20, blank=True, null=True)

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

class OrganizationAddress(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Опционально

    class Meta:
        unique_together = ('organization', 'address')  # Запрет дублирования

    def __str__(self):
        return (
            f"{self.organization.name} → {self.address} "
            f"(добавлен {self.created_at.strftime('%Y-%m-%d')})"
        )

class OrganizationService(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    is_main_service = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.DurationField('Длительность оказания', null=True)

    class Meta:
        unique_together = ('organization', 'service')

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

    target_groups = models.ManyToManyField(
        TargetGroup,
        verbose_name='Целевые группы',
        blank=True
    )

    address = models.ManyToManyField(
        Address, 
        through='OrganizationAddress',  # Указываем промежуточную модель
        verbose_name="Адрес",
        blank=True
    )
    
    # Для услуг используем промежуточную модель
    services = models.ManyToManyField(
        Service,
        through='OrganizationService',
        verbose_name='Услуги',
        blank=True
    )

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['name']

    def __str__(self):
        return self.name

class ContactInfo(models.Model):
    """Универсальная модель контактной информации"""
    class ContactType(models.TextChoices):
        PHONE = 'phone', 'Телефон'
        EMAIL = 'email', 'Email'
        ADDRESS = 'address', 'Адрес'
        WEBSITE = 'website', 'Сайт'
        SOCIAL = 'social', 'Соцсеть'
        OTHER = 'other', 'Другое'

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='contacts'
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
        related_name='working_schedules'
    )
    day_of_week = models.IntegerField(
        'День недели',
        choices=DayOfWeek.choices
    )
    opens_at = models.TimeField('Время открытия', null=True, blank=True)
    closes_at = models.TimeField('Время закрытия', null=True, blank=True)
    is_round_the_clock = models.BooleanField('Круглосуточно', default=False)
    is_closed = models.BooleanField('Выходной', default=False)
    comment = models.CharField('Комментарий', max_length=100, blank=True)

    class Meta:
        verbose_name = 'График работы'
        verbose_name_plural = 'Графики работы'
        ordering = ['day_of_week']

    def __str__(self):
        if self.is_closed:
            return f"{self.get_day_of_week_display()}: {'Выходной'}"
        if self.is_round_the_clock:
            return f"{self.get_day_of_week_display()}: {'Круглосуточно'}"
        return f"{self.get_day_of_week_display()}: {self.opens_at} - {self.closes_at}"

class GeoLocation(models.Model):
    """Геолокация организации"""
    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        related_name='geo_location'
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
        related_name='social_profiles'
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
        related_name='programs'
    )
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    start_date = models.DateField('Дата начала', null=True, blank=True)
    end_date = models.DateField('Дата окончания', null=True, blank=True)
    target_groups = models.ManyToManyField(
        TargetGroup,
        verbose_name='Целевые группы',
        blank=True
    )
    is_free = models.BooleanField('Бесплатно', default=True)
    participation_conditions = models.TextField('Условия участия', blank=True)

    class Meta:
        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} ({self.organization})"