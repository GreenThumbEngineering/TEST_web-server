from django.db import models
from customuser.models import User as custom_user
from datetime import datetime

class PlantData(models.Model):
  DeviceId = models.CharField(max_length = 20, default='')
  SystemId = models.CharField(max_length = 20, default='')
  MeasurementTime = models.DateTimeField(default=datetime.now)
  ServerTime = models.DateTimeField(default=datetime.now)
  Temperature = models.FloatField(default=0)
  Humidity = models.FloatField(default=0)
  SoilMoisture = models.IntegerField(default=0)
  Luminosity = models.IntegerField(default=0)
  GivenWater = models.FloatField(default=0)
  Temperature_pred = models.FloatField(default=0)
  Luminosity_pred = models.FloatField(default=0)
  SoilMoisture_pred = models.FloatField(default=0)
  NDVI_pred = models.FloatField(default=0)


class Plants(models.Model):
  user = models.ForeignKey(custom_user,on_delete=models.CASCADE)
  nickname = models.CharField(max_length=20, blank=True)
  deviceid = models.CharField(max_length=20)
  plant_pic = models.ImageField(upload_to='plant_pics', blank=True)

class NDVIMeasurement(models.Model):
  MeasurementTime = models.DateTimeField(default=datetime.now)
  Plant = models.ForeignKey(Plants,on_delete=models.CASCADE)
  NDVI_value = models.FloatField(blank=False)

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