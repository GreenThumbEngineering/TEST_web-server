from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
  author = models.CharField(max_length = 20)
  title = models.CharField(max_length = 40)
  publication_year = models.IntegerField()
  
class PlantData(models.Model):
  deviceID = models.CharField(max_length = 20, default='')
  Time = models.CharField(max_length = 40, default='')
  Temperature = models.FloatField(default=0)
  Humidity = models.FloatField(default=0)
  Pressure = models.FloatField(default=0)
  Soil = models.IntegerField(default=0)
  ColorTemp = models.IntegerField(default=0)
  Lux = models.FloatField(default=0)
  RGB = models.CharField(max_length = 20, default='')

class Plants(models.Model):
  userid = models.IntegerField()
  nickname = models.CharField(max_length=30)
  deviceid = models.CharField(max_length=300, unique=True)
  
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)


def __str__(self):
    return self.user.username