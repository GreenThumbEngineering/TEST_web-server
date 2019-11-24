from django.db import models
from colorful.fields import RGBColorField


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
  
