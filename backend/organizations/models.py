from django.db import models
from servises.models import Servis
from assistance.models import Assistance

class Region(models.Model):
    name = models.CharField("Область", max_length=100)

class SubRegion(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField("Муниципалитеты", max_length=100)
 
class City(models.Model):
    sub_region = models.ForeignKey(SubRegion, on_delete=models.CASCADE)
    name = models.CharField("Город", max_length=100)

class CityRegion(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField("Округ", max_length=100)

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
    
# class Address(models.Model):
#     city_region = models.ForeignKey(CityRegion, on_delete=models.SET_NULL)
#     street = models.CharField("Улица", max_length=100)
#     house = models.CharField("Дом", max_length=20)
#     apartment = models.CharField("Квартира", max_length=20, blank=True, null=True)
#     #postcode

# 	def __str__(self):
#         return f"{self.city.region}, {self.city}, {self.street}, {self.house}" + (f", кв. {self.apartment}" if self.apartment else "")


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
    # logo = models.ImageField(upload_to="org_logos/")
    # website = models.URLField("Сайт")
    update_date = models.DateField("Дата обновления данных", auto_now=True)

    # Контактные данные
    address = models.ManyToManyField(Address, verbose_name="Адрес")
    # phone = models.CharField("Телефон", max_length=20)
    # email = models.EmailField("Email")

    # Рабочее время
    # work_hours = models.TextField("Режим работы")

    # Геоданные
    # latitude = models.FloatField("Широта")
    # longitude = models.FloatField("Долгота")
    
    """Связи"""
    assistance = models.ManyToManyField(Assistance, related_name='Помощь', verbose_name='Категории', null=True, blank=True)
    services = models.ManyToManyField(Servis, related_name='Услуги', verbose_name='Услуги', null=True, blank=True)
    # event = models.ManyToManyField(Event, verbose_name="Мероприятия")
	

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['name']

    def __str__(self):
        return self.name


# class OrganizationService(models.Model):
#     organization = models.ForeignKey(
#         Organization, on_delete=models.CASCADE, related_name="services"
#     )
#     title = models.CharField("Услуга", max_length=200)
#     description = models.TextField("Описание")
#     eligibility = models.TextField("Условия получения")
#     documents = models.TextField("Необходимые документы")
#     legal_basis = models.TextField("Правовая основа")
#     start_date = models.DateField("Дата начала")
#     end_date = models.DateField("Дата окончания", null=True, blank=True)
