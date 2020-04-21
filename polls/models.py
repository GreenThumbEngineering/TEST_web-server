from django.db import models
from customuser.models import User as custom_user
from datetime import datetime
from django.utils import timezone

class PlantData(models.Model):
  DeviceId = models.CharField(max_length = 20, default='')
  SystemId = models.CharField(max_length = 20, default='')
  MeasurementTime = models.DateTimeField(default=timezone.now)
  ServerTime = models.DateTimeField(default=timezone.now)
  Temperature = models.FloatField(default=0)
  Humidity = models.FloatField(default=0)
  SoilMoisture = models.IntegerField(default=0)
  Luminosity = models.IntegerField(default=0)
  White_pic = models.ImageField(upload_to='images')
  Nir_pic = models.ImageField(upload_to='images')

  grades = (
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
  )

  NDVI_grade = models.IntegerField(blank=True, null=True, choices=grades, default=None)
  NDVI_value = models.FloatField(blank=True, null=True, default=None)
  VPD = models.FloatField(default=0)



class Plants(models.Model):
  user = models.ForeignKey(custom_user,on_delete=models.CASCADE)
  nickname = models.CharField(max_length=20, blank=True)
  deviceid = models.CharField(max_length=20)
  plant_pic = models.ImageField(upload_to='images', blank=True)
  sizes = [
    ('small', 'Small'),
    ('medium', 'Medium'),
    ('large', 'Large')
  ]
  plantpot_size = models.CharField(choices=sizes, default='medium', max_length=20)
  types = [
    ('basil', 'Basil'),
    ('other', 'Other')
  ]
  plant_type = models.CharField(choices=types, default='basil', max_length=20)


class Water(models.Model):
  MeasurementTime = models.DateTimeField(default=datetime.now)
  Plant = models.ForeignKey(Plants,on_delete=models.CASCADE)
  WaterAdded = models.FloatField(blank=False)
  
class UserProfileInfo(models.Model):
  user = models.OneToOneField(custom_user, on_delete=models.CASCADE)
  portfolio_site = models.URLField(blank=True)
  profile_pic = models.ImageField(upload_to='profile_pics',blank=True)


def __str__(self):
    return self.user.username