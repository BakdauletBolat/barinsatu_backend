from statistics import mode
from tabnanny import verbose
from django.db import models
from authentication.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class AdType(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип публикаций'
        verbose_name_plural = 'Типы публикаций'

class AdDetailType(models.Model):
    
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        
        verbose_name = 'Тип детальной информаций'
        verbose_name_plural = 'Тип детальной информаций'

class City(models.Model):

    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

    class Meta:
        
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

class RentType(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        
        verbose_name = 'Время аренды'
        verbose_name_plural = 'Время аренды'


class BuildingType(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        
        verbose_name = 'Тип построение'
        verbose_name_plural = 'Тип построение'

class RepairType(models.Model):
    
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        
        verbose_name = 'Тип ремонта'
        verbose_name_plural = 'Типы ремонта'


class HomeDetail(models.Model):

    numbers_room = models.IntegerField(null=True,blank=True)
    total_area = models.IntegerField(null=True,blank=True)
    floor = models.IntegerField(null=True,blank=True)
    year_construction = models.IntegerField(null=True,blank=True)
    building_type = models.ForeignKey(BuildingType,on_delete=models.CASCADE)
    repair_type = models.ForeignKey(RepairType,on_delete=models.CASCADE)

    def __str__(self):

        return self.building_type.name

    class Meta:
        
        verbose_name = 'Дом дополнение публикаций'
        verbose_name_plural = 'Дом дополнение публикаций'


class AreaDetail(models.Model):
    
    area = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.area

    class Meta:
        
        verbose_name = 'Участок дополнение публикаций'
        verbose_name_plural = 'Участок дополнение публикаций'


class Ad(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveBigIntegerField()

    ad_detail_type = models.ForeignKey(AdDetailType,on_delete=models.CASCADE,null=True,blank=True,related_name='ads')
    ad_type = models.ForeignKey(AdType,on_delete=models.CASCADE,related_name='ads')
    city = models.ForeignKey(City,on_delete=models.CASCADE,related_name='ads')
    rent_time = models.ForeignKey(RentType,on_delete=models.CASCADE,null=True,blank=True,related_name='ads')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,related_name='ads',null=True,blank=True)
    object_id = models.PositiveIntegerField(null=True,blank=True)
    details = GenericForeignKey('content_type', 'object_id')

    location_text = models.CharField(max_length=255,null=True,blank=True)
    lat = models.FloatField(null=True,blank=True)
    lng = models.FloatField(null=True,blank=True)

    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ads')

    def __str__(self):

        return self.title

    class Meta:
    
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикаций'


class AdImage(models.Model):

    image = models.ImageField(upload_to='AdImage/')
    ad = models.ForeignKey(Ad,on_delete=models.CASCADE,related_name='images')

    class Meta:

        verbose_name = 'Фотография для Публикаций'
        verbose_name_plural = 'Фотографий для Публикаций'
