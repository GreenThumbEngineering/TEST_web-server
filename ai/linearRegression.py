import numpy as np
from scipy import stats

# timeInterval = no. of points used to make prediction
def makeLinReg(plantdata, timeInterval, lineRange = None):
    """timeInterval = no. of points used to make prediction"""
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
    """
    plantList : list\n
    slope, intercept from 'makeLinReg' function\n
    noOfPreds : int
        number of predictions (default = 1)
    """
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

def getLinearData(deviceID, temperatures, luminosities, soilMoistures, timeInterval):
    """
    Parameters
    ----
    temperatures : list

    luminosities : list

    soilMoistures : list

    timeInterval : tuple
        (starting point, ending point)
    Returns
    ------
    tuple
        (tempPred, lumPred, soilMoistPred)
    """
    xregTemp, yregTemp, tempSlope, tempIntercept, rValTemp = makeLinReg(temperatures, timeInterval)
    xregLum, yregLum, LumSlope, LumIntercept, rValLum = makeLinReg(luminosities, timeInterval)
    xregSoilMoist, yregSoilMoist, SoilMoistSlope, SoilMoistIntercept, rValSoilMoist = makeLinReg(soilMoistures, timeInterval)

    tempPred = makePred(temperatures, tempSlope, tempIntercept)[1]
    lumPred = makePred(luminosities, LumSlope, LumIntercept)[1]
    soilMoistPred = makePred(soilMoistures, SoilMoistSlope, SoilMoistIntercept)[1]

    return (deviceID, tempPred, lumPred, soilMoistPred)
