from django.db import models
from datetime import datetime

class PlantPrediction(models.Model):
  DeviceID = models.CharField(max_length = 20, default='')
  Timestamp = models.DateTimeField(default=datetime.now())
  Temperature_pred = models.FloatField(default=0)
  Luminosity_pred = models.FloatField(default=0)
  SoilMoisture_pred = models.FloatField(default=0)
  NDVI_pred = models.FloatField(default=0)