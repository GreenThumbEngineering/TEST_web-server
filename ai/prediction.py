from polls.models import PlantData
from ai.models import PlantPrediction

from linearRegression import getLinearData

objects = PlantData.objects.all()
data = [obj for obj in objects]

temperatures = [val.Temperature for val in data]
luminosities = [val.Luminosity for val in data]
soilMoistures = [val.SoilMoisture for val in data]
deviceIDs = [val.DeviceId for val in data]

# linear regression predictions
tempPred, lumPred, soilMoistPred = getLinearData(deviceIDs, temperatures, luminosities, soilMoistures, (0, 18)) 

PlantPrediction.objects.create(DeviceID=deviceIDs,Temperature_pred=tempPred, Luminosity_pred=lumPred, SoilMoisture_pred=soilMoistPred)