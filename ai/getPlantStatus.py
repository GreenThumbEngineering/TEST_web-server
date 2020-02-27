from polls.models import PlantData
from plantStatus import inTheDark, needsWater

def getData(deviceID):
    objects = PlantData.objects.filter(DeviceId=deviceID).order_by('-ServerTime')
    data = [obj for obj in objects]

    print(data[0].SoilMoisture)

    return (needsWater(data.soilMoisture), inTheDark(data.luminosity))