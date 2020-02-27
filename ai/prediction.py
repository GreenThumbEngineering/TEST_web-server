from polls.models import PlantData
from ai.models import PlantPrediction

import numpy as np
from scipy import stats

# timeInterval = no. of points used to make prediction
def makeLinReg(plantdata, timeInterval, lineRange = None):
    l = len(plantdata)
    x = list(range(l))
    y = plantdata

    slope, intercept, r_value, p_value, std_err = stats.linregress(x[timeInterval[0]:timeInterval[1]], y[timeInterval[0]:timeInterval[1]])

    if lineRange is not None:
        xreg = np.array(list(range(lineRange)))
    else:
        xreg = np.array(list(range(l)))

    yreg = slope * xreg + intercept
    
    return (xreg, yreg, slope, intercept, r_value)

# plantList = "temps", slope and interecept from 'makeLinReg' function
def makePred(plantList, slope, intercept, noOfPreds = 1):
    l = len(plantList)
    x = list(range(l))

    predX = []
    predY = []

    if noOfPreds == 1:
        predX.append(x[-1] + noOfPreds) # = [(x[-1] + noOfPreds, slope * (x[-1] + noOfPreds) + intercept)]
        predY.append(slope * (x[-1] + noOfPreds) + intercept)
    else:
        for i in range(1, noOfPreds + 1):
            predX.append(x[-1] + i)
            predY.append(slope * (x[-1] + i) + intercept)

    predX = np.array(predX)
    predY = np.array(predY)
    
    return (predX, predY)


def main():
    objects = PlantData.objects.all()
    data = [obj for obj in objects]

    temperatures = [val.Temperature for val in data]
    luminosities = [val.Luminosity for val in data]
    soilMoistures = [val.SoilMoisture for val in data]

    xregTemp, yregTemp, tempSlope, tempIntercept, rValTemp = makeLinReg(temperatures, (0, 18))
    xregLum, yregLum, LumSlope, LumIntercept, rValLum = makeLinReg(luminosities, (0, 18))
    xregSoilMoist, yregSoilMoist, SoilMoistSlope, SoilMoistIntercept, rValSoilMoist = makeLinReg(soilMoistures, (0, 18))

    tempPred = makePred(temperatures, tempSlope, tempIntercept)[1]
    lumPred = makePred(luminosities, LumSlope, LumIntercept)[1]
    soilMoistPred = makePred(soilMoistures, SoilMoistSlope, SoilMoistIntercept)[1]

    PlantPrediction.objects.create(Temperature_pred=tempPred, Luminosity_pred=lumPred, SoilMoisture_pred=soilMoistPred)

    # for row in data:
    #     dataInDB = PlantPrediction.objects.create(Temperature_pred=row.Temperature, Luminosity_pred=row.Luminosity, SoilMoisture_pred=row.SoilMoisture)

    {
        # for luminosity in data:
        #     luminosityInDB = PlantPrediction.objects.create(Luminosity_pred=luminosity)

        # for soilMoisture in data:
        #     soilMoistureInDB = PlantPrediction.objects.create(SoilMoisture_pred=soilMoisture)
    }

main()