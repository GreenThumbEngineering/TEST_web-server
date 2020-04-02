from math import exp

class VPD:
    
    def calcvpd(temperature, humidity):
        airTemp = temperature
        leafTemp = temperature - 2
        vpAIR = 610.78 * exp(airTemp / (airTemp + 238.3) * 17.2694)/1000
        vpLEAF = 610.78 * exp(leafTemp / (leafTemp + 238.3) * 17.2694)/1000
        vpd = vpLEAF - (vpAIR * humidity/100)
        return vpd
