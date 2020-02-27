from django.db import models

class PlantPrediction(models.Model):
  Temperature_pred = models.FloatField(default=0)
  Luminosity_pred = models.FloatField(default=0)
  SoilMoisture_pred = models.FloatField(default=0)
  NDVI_pred = models.FloatField(default=0)