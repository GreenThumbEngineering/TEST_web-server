from polls.models import PlantData
from ai.models import PlantPrediction
from ai.linearRegression import getLinearData
from datetime import timedelta

def makePredictions(deviceID, noOfDatapoints, noOfPredictions = 1):
    objects = PlantData.objects.filter(DeviceId=deviceID).order_by('-ServerTime')
    data = [obj for obj in objects][:48] # 48 latest measurements --> latest 24 hours
    data.reverse()
    temperatures = [val.Temperature for val in data]
    luminosities = [val.Luminosity for val in data]
    soilMoistures = [val.SoilMoisture for val in data]
    times = [val.ServerTime for val in data]
    latestTime = times[-1]
    predictedTimestamps = []
    for i in range(1, noOfPredictions + 1):
        predictedTimestamps.append(latestTime + i *  timedelta(minutes=30))
    tempPred, lumPred, soilMoistPred = getLinearData(temperatures, luminosities, soilMoistures, noOfDatapoints, noOfPredictions)
    # PlantPrediction.objects.create(DeviceID=deviceID)
    for i in range(noOfPredictions):
        PlantPrediction.objects.create(DeviceID=deviceID,
                                       Timestamp=predictedTimestamps[i],
                                       Temperature_pred=tempPred[i],
                                       Luminosity_pred=lumPred[i], 
                                       SoilMoisture_pred=soilMoistPred[i])

# makePredictions('ESP32-4886A6C40A24', (0, 18), 5)