from polls.models import PlantData
from ai.plantStatus import inTheDark, needsWater

def getData(deviceID):
    objects = PlantData.objects.filter(DeviceId=deviceID).order_by('-ServerTime')
    data = [obj for obj in objects]
    return (needsWater(data[0].SoilMoisture), inTheDark(data[0].Luminosity))

# getData("ESP32-39508D2DE6B4")