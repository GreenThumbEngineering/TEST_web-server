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
  Temp_pred = models.FloatField(default=0)
  Luminosity_pred = models.FloatField(default=0)
  SoilMoist_pred = models.FloatField(default=0)
  NDVI_pred = models.FloatField(default=0)

class Plants(models.Model):
  userid = models.IntegerField()
  nickname = models.CharField(max_length=30)
  deviceid = models.CharField(max_length=30)
  
class UserProfileInfo(models.Model):
  user = models.OneToOneField(custom_user, on_delete=models.CASCADE)
  portfolio_site = models.URLField(blank=True)
  profile_pic = models.ImageField(upload_to='profile_pics',blank=True)


def __str__(self):
    return self.user.username