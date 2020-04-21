from math import exp

class VPD:
    
    def calcvpd(temperature, humidity):
        airTemp = temperature
        leafTemp = temperature - 2
        vpAIR = 610.78 * exp(airTemp / (airTemp + 238.3) * 17.2694)/1000
        vpLEAF = 610.78 * exp(leafTemp / (leafTemp + 238.3) * 17.2694)/1000
        vpd = vpLEAF - (vpAIR * humidity/100)
        return vpd

    defaultNormalStatusText = "<p>Everything seems to be in order.</p>"

    def ndviAnalysis(ndvi): #TODO make this 
        if ndvi != None:

        #HEURESTICS AND THRESHOLDS

            #MATCHING NDVI WITH VALUES 1-5
            #THRESHOLDS: 0.35+ EXCELLENT 0.3+ GOOD 0.25 OKAY 0.2 BAD 0.1- RLY BAD/DEAD
            optimalRange = ndvi >= 0.35
            goodRange = ndvi >= 0.28
            okayRange = ndvi >= 0.21
            deadRange = ndvi < 0.13
            badRange = ndvi < 0.21

            gradeDescriptions = ["critically low","pretty low","okay","quite good","excellent"]
            ndvi_grade = 0 #initial
            #order is essential
            if optimalRange:
                ndvi_grade = 5
            elif goodRange:
                ndvi_grade = 4
            elif okayRange:
                ndvi_grade = 3
            elif deadRange:
                ndvi_grade = 1
            elif badRange:
                ndvi_grade = 2
        #STATUSTEXTS
        
            generalStatusText = "<p>The current NDVI is looking {}, at {:.2f}.</p>".format(gradeDescriptions[ndvi_grade-1],ndvi)
        
        #EXPLANATIONS
        
            generalExplanation = "<p>Normalized Difference Vegetation Index (NDVI) quantifies the health of a plant. The higher the NDVI, the healthier the plant! NDVI is calculated by measuring the difference between near-infrared light (which vegetation strongly reflects) and red light (which healthy vegetation absorbs).</p>"
        
        #INSTRUCTIONS
            generalInstruction = "<p>Always keep an eye out for the NDVI!</p>"
            optimalInstructions = "<p>Keep doing what you're doing!</p>"
            goodInstructions = "<p>Keep doing what you're doing!</p>"
            okayInstructions = "<p>Try to look at the other measures of plant health, and see if there would be something to do.</p>"
            badInstructions = "<p>Look at the other measures of plant health, and see if there would be something to do.</p>"
            deadInstructions = "<p>Look at the other measures of plant health, and see if there would be something to do.</p>"
        #OUTPUT

            if optimalRange:
                return(False,generalStatusText,generalExplanation,optimalInstructions)
            elif goodRange:
                return(False,generalStatusText,generalExplanation,goodInstructions)
            elif okayRange:
                return(False,generalStatusText,generalExplanation,okayInstructions)
            elif deadRange:
                return(True,generalStatusText,generalExplanation,deadInstructions)
            elif badRange:
                return(True,generalStatusText,generalExplanation,badInstructions)
        else:
            #NDVI was "None"
            return(True,"<p>There was an error in the most recent ndvi measurement.</p>","<p>Normalized Difference Vegetation Index (NDVI) quantifies the health of a plant. The higher the NDVI, the healthier the plant! NDVI is calculated by measuring the difference between near-infrared light (which vegetation strongly reflects) and red light (which healthy vegetation absorbs).</p>","<p>Check that the camera is positioned right.</p>")


    def vpdAnalysis(humidity, temperature):
        
        #VPD CALCULATION
            def calculateVpd(humidity, temperature):
                airTemp = temperature
                leafTemp = temperature - 2 #This is a guess for now, usually leaf temperatures are 1-3C lower than the air temperature
                from math import exp
                #the formula was taken from this site https://pulsegrow.com/blogs/learn/vpd
                vpAIR = 610.78 * exp(airTemp / (airTemp + 238.3) * 17.2694)/1000
                vpLEAF = 610.78 * exp(leafTemp / (leafTemp + 238.3) * 17.2694)/1000
                vpd = vpLEAF - (vpAIR * humidity/100)
                return vpd
            vpd = calculateVpd(humidity, temperature)
            #VPD has now been calculated.
        
        #HELP FUNCTIONS TODO: remove these or leave them?
            def calculateHum(T, V):
                #vpd = 610.78 * exp( (temperature - 2)  / (temperature - 2  + 238.3) * 17.2694)/1000 - (610.78 * exp(temperature / (temperature + 238.3) * 17.2694)/1000 * humidity/100)
                #wolfram says:
                from math import exp
                H = 0.0032745 * exp(-(17.2694 * T)/(T + 238.3) - 34.5388/(T + 236.3)) * (30539 * exp((17.2694 * T)/(T + 236.3)) - 50000 * exp(34.5388/(T + 236.3)) * V)
                if H - humidity  > 100: #Relative humidity over 100% would be recommended
                    H = 100  #this - humidity
                elif H - humidity < 0: #Relative humidity under 0% would be recommended
                    H = 0 #this - humidity
                return H
            def calculateTemp(H, V):
                #vpd = 610.78 * exp( (temperature - 2)  / (temperature - 2  + 238.3) * 17.2694)/1000 - (610.78 * exp(temperature / (temperature + 238.3) * 17.2694)/1000 * humidity/100)
                #wolfram says: too long to compute..
                goodVList = []
                for t in range((30 + int(abs(temperature)))*3):    #Really dumb implementation, could act weird when the vpd is almost between 2 ranges
                    distanceFromGoodV = V - calculateVpd(H, t)
                    goodVList.append(abs(distanceFromGoodV))
                return goodVList.index(min(goodVList))  #this value of t is the closest to the one we're looking for.
                

        #STATUSTEXTS
            optimalStatusText = "<p>The plant's VPD (vapor pressure deficit) is looking great!</p>"
            slightlyLowStatusText = "<p>The plant's VPD (vapor pressure deficit)is looking okay, but it could be a little bit higher.</p>"
            slightlyHighStatusText = "<p>The plant's VPD (vapor pressure deficit)is looking okay, but it could be a little bit lower.</p>"
            tooLowStatusText = "<p>ATTENTION! The plant's VPD (vapor pressure deficit) is looking critically low.</p>"
            tooHighStatusText = "<p>ATTENTION! The plant's VPD (vapor pressure deficit) is looking critically high.</p>"
        #EXPLANATIONS
            tooLowExplanation = "<p>A low VPD means the air quality around your plant makes it hard for it to transpire enough. This will make it hard for the plant to absorb nutrients leading to nutrient deficiency issues, and potentially mold growth.</p>"
            #slightlyLowExplanation = "<p>If the air is cold or damp, less moisture is pulled from the plant, meaning fewer nutrients go into the plant and the plant might develop deficiencies and mould or freeze and die.</p>"
            #slightlyHighExplanation = "<p>If the air is hot or dry, the difference in vapor pressure can be too great and can cause plants to become stressed under rapid transpiration. This can result in nutrient toxicity due to excessive uptake of nutrients (even if fed with just water).[ One of these nutrient overloads may be calcium, which can lead to chlorosis and stunted growth.]</p>"
            tooHighExplanation = "<p>A high VPD means the air around your plant is having a major drying effect on it. This makes the plant transpire too much, which causes it stress. The plant can absorb too much nutrients, which leads to toxicity and other issues.</p>"
            generalExplanation = "<p>The VPD (vapor pressure deficit) of a plant is a measure of the drying effect of the air around the plant. A high VPD means a major drying effect, while a low VPD means a minimal drying effect. Too high of a VPD will lead to the plant transpiring a lot, causing it to absorb excessive nutrients from the soil and leading to nutrient toxicity. If the VPD is especially high, the plant closes its stomata (airways), and stops growing to save water. This closing of the stomata stops the plant from producing energy through photosynthesis. Too low of a VPD on the other hand will lead to the plant not being able to transpire enough, and will thus make it harder for the plant to absorb nutrients from the soil. This can result in a nutrient deficiency, and can ultimately lead to the plant freezing or dying.</p>"
        #INSTRUCTIONS
            optimalInstructions = "<p>No need to do anything!</p>" 
            slightlyHighInstructions = "<p>Try changing the temperature by {:+.1f} degrees, or changing the humidity by {:+.1f} % to make the vpd even better!</p>".format(calculateTemp(humidity, 1.15) - temperature,calculateHum(temperature, 1.15) - humidity )
            slightlyLowInstructions = "<p>Try changing the temperature by {:+.1f} degrees, or changing the humidity by {:+.1f} % to make the vpd even better!</p>".format(calculateTemp(humidity, 1.15) - temperature,calculateHum(temperature, 1.15) - humidity )
            tooHighInstructions = "<p>Try to change the temperature by [at least] {:+.1f} degrees, or change the humidity by [at least] {:+.1f} percent as quickly as possible! For an optimal vpd, a change of {:+.1f} degrees or {:+.1f} percent is required.</p>".format(calculateTemp(humidity, 1.45) - temperature,calculateHum(temperature, 1.45) - humidity,calculateTemp(humidity, 1.15) - temperature,calculateHum(temperature, 1.15) - humidity)
            tooLowInstructions = "<p>Try to change the temperature by [at least] {:+.1f} degrees, or change the humidity by [at least] {:+.1f} percent as quickly as possible! For an optimal vpd, a change of {:+.1f} degrees or {:+.1f} percent is required.</p>".format(calculateTemp(humidity, 0.9) - temperature,calculateHum(temperature, 0.9) - humidity,calculateTemp(humidity, 1.15) - temperature,calculateHum(temperature, 1.15) - humidity)
        #HEURESTICS AND THRESHOLDS

            #TODO: When we have many plant types, we should have PLANTTYPE.highVpdThreshold etc. Now we focus only on Basil.
            #These ranges are "best guesses", hard to find info for optimal vpds for basilica. Need to test what we get with our data.
            optimalRange = vpd >= 1 and vpd <= 1.3
            slightlyHighRange = (vpd <= 1.6 and vpd > 1.3)
            slightlyLowRange = (vpd >= 0.8 and vpd < 1)
            tooHighRange = vpd > 1.6
            tooLowRange = vpd < 0.8

            print(vpd)
            if optimalRange:
                # "Temp = {}, Hum = {}, VPD = {}.".format(temperature, humidity, vpd)
                return(False, optimalStatusText, generalExplanation, optimalInstructions)
            elif slightlyHighRange:
                return(False, slightlyHighStatusText, tooHighExplanation, slightlyHighInstructions)
            elif slightlyLowRange:
                return(False, slightlyLowStatusText, tooLowExplanation, slightlyLowInstructions)
            elif tooHighRange:
                return(True, tooHighStatusText, tooHighExplanation, tooHighInstructions)
            elif tooLowRange:
                return(True, tooLowStatusText, tooLowExplanation, tooLowInstructions)
            else:
                #error
                return(True, "<p>error</p>","<p>error</p>","<p>error</p>")
