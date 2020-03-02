from polls.models import PlantData
from ai.plantStatus import vpdAnalysis, tempAnalysis, humAnalysis, soilAnalysis, lumAnalysis#inTheDark, needsWater

def getData(deviceID):
    objects = PlantData.objects.filter(DeviceId=deviceID).order_by('-ServerTime')
    data = [obj for obj in objects]
    return(vpdAnalysis(data[0].Temperature,data[0].Humidity),tempAnalysis(data[0].Temperature),humAnalysis(data[0].Humidity),soilAnalysis(data[0].SoilMoisture),lumAnalysis(data[0].Luminosity))#return (needsWater(data[0].SoilMoisture), inTheDark(data[0].Luminosity))

# getData("ESP32-39508D2DE6B4")