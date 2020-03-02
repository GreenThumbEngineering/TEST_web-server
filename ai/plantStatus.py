def inTheDark(luminosity):
    """
    Returns
    --------
    0
        if everything is good / sun is up
    1
        if it's starting to be dark / is dark
    """
    if luminosity < 20:
        return 1
    else:
        return 0

def needsWater(soilMoisture):
    """
    Returns
    --------
    -1
        if too much water?
    0
        if everything is good
    1
        if needs watering soon
    2
        if needs watering right away
    """

    # if soilMoisture >= 2600: # when is too much water?
    #     return -1
    # elif 2200 <= soilMoisture < 2600:
    #     return 0
    # elif 1400 <= soilMoisture < 2200:
    #     return 1
    # else:
    #     return 2
    return "water statusText test placeholder"
        
    
#ANALYSIS FUNCTIONS:    
#TODO: refactor the Analysis functions into 2 functions: one that outputs a state (1-5) and information about how far the values are from the optimal values, and one that outputs (statusText, explanation, instructions). Maybe even combine all the different parameter analyses into 1 function
#TODO: make a "neutral explanation" variable to all analysis functions.

#"global" variables
defaultNormalStatusText = "Everything seems to be in order."

def vpdAnalysis(humidity, temperature):
    #STATUSTEXTS    #TODO: make the variable names of VPD statusTexts consistent with the other functions
        optimalVpdStatusText = "PLANTNAME's VPD (vapor pressure deficit) is looking great."
        #With this implementation it's impossible to know X or Y.
        okayVpdStatusText = "PLANTNAME's VPD (vapor pressure deficit)is looking okay, but it could be better. Changing the temperature by X degrees, or changing the humidity by Y % would make it even better!"
        #With this implementation it's impossible to know X or Y.
        badVpdStatusText = "ATTENTION! PLANTNAME's VPD (vapor pressure deficit) is looking critically bad. Try to change the temperature by [at least] X degrees, or change the humidity by [at least] Y percent as quickly as possible!"
    #EXPLANATIONS
        coldOrDampExplanation = "If the air is cold or damp, less moisture is pulled from the plant, meaning fewer nutrients go into the plant and the plant might develop deficiencies and mould or freeze and die."
        slightlyHotOrDry = "If the air is hot or dry, the difference in vapor pressure can be too great and can cause plants to become stressed under rapid transpiration. This can result in nutrient toxicity due to excessive uptake of nutrients (even if fed with just water).[ One of these nutrient overloads may be calcium, which can lead to chlorosis and stunted growth.]"
        tooHotOrDry = "If the air is too hot or dry, the plant stops growing to save water and closes the cells that release moisture and enable photosynthesis[ (located on the underside of the leaf, called the stomata cells)]."
    #INSTRUCTIONS
        instructions = "placeholder" #TODO
    
    #TODO: Choose the right strings according to some heurestics. In vpd's case, implement with a matrix of temp and hum data's relationships.
        return(badVpdStatusText, tooHotOrDry, instructions) #arbitrarily chosen for now

def tempAnalysis(temperature):
    #STATUSTEXTS
        criticallyLowStatusText = "ATTENTION! PLANTNAME's temperature is critically low!\nPLANTTYPE.name s are recommended to be kept at ???~???*C, PLANTNAME is currently RECOMMENDEDTEMP-PLANTTEMP lower."
        slightlyLowStatusText = "It looks like the temperature of PLANTNAME has gone under the recommended level.\nPLANTTYPE.name s are recommended to be kept at ???~???*C, PLANTNAME is currently RECCOMENDEDTEMP-PLANTTEMP lower."
        normalStatusText = defaultNormalStatusText
        slightlyHighStatusText = "It looks like the temperature of PLANTNAME has gone over the recommended level.\nPLANTTYPE.name s are recommended to be kept at ???~???*C, PLANTNAME is currently PLANTTEMP-RECCOMENDEDTEMP higher."
        criticallyHighStatusText = "ATTENTION! PLANTNAME's Temperature is critically high!\nPLANTTYPE.name s are recommended to be kept at ???~???*C, PLANTNAME is currently PLANTTEMP-RECOMMENDEDTEMP higher."
    #EXPLANATIONS
        #Need more knowledge to make a good explanation  
        highExplanation = "Having a higher temperature makes it harder for PLANTTYPE.name to do photosynthesis. NAR...(something)..."
        lowExplanation = "Having a lower temperature makes it harder for PLANTTYPE.name to do photosynthesis. NAR...(something)..."    

    #INSTRUCTIONS
        instructions = "placeholder" #TODO

    #TODO: Choose the right strings according to some heurestics
        return(criticallyLowStatusText, lowExplanation, instructions) #arbitrarily chosen for now

def humAnalysis(humidity): #is this useful? is vpd enough?
    #STATUSTEXTS
        criticallyLowStatusText = "ATTENTION! PLANTNAME's humidity is critically low!\nPLANTTYPE.name s are recommended to be kept at ???~???% relative humidity, PLANTNAME is currently RECOMMENDEDHUM-PLANTHUM lower."
        slightlyLowStatusText = "It looks like the humidity of PLANTNAME has gone under the recommended level.\nPLANTTYPE.name s are recommended to be kept at ???~???*C, PLANTNAME is currently RECCOMENDEDHUM-PLANTHUM lower."
        normalStatusText = defaultNormalStatusText
        slightlyHighStatusText = "It looks like the humidity of PLANTNAME has gone over the recommended level.\nPLANTTYPE.name s are recommended to be kept at ???~???*C, PLANTNAME is currently PLANTHUM-RECCOMENDEDHUM higher."
        criticallyHighStatusText = "ATTENTION! PLANTNAME's humidity is critically high!\nPLANTTYPE.name s are recommended to be kept at ???~???% relative humidity, PLANTNAME is currently PLANTHUM-RECOMMENDEDHUM higher."
    #EXPLANATIONS
        #Need more knowledge to make a good explanation. (also does hum matter for anything else than vpd?)
        highExplanation = "Being in a highly humid environment makes it harder for PLANTTYPE.name to do photosynthesis. ...(something)..."
        lowExplanation = "Being in a highly dry environment makes it harder for PLANTTYPE.name to do photosynthesis. ...(something)..."
    #INSTRUCTIONS
        instructions = "placeholder" #TODO

    #TODO: Choose the right strings according to some heurestics
        return(slightlyHighStatusText, highExplanation, instructions) #arbitrarily chosen for now

def soilAnalysis(soilMoisture):
    #STATUSTEXTS
        criticallyLowStatusText = "ATTENTION! PLANTNAME's soil moisture is critically low!\nPLANTTYPE.name 's soil moisture is at best when around ???~??? UNITs, PLANTNAME is currently RECOMMENDEDSOIL-PLANTSOIL lower."
        slightlyLowStatusText = "It looks like the soil moisture of PLANTNAME has gone under the recommended level.\nPLANTTYPE.name 's soil moisture is at best when around ???~??? UNITs, PLANTNAME 's is currently RECCOMENDEDSOIL-PLANTSOIL lower."
        normalStatusText = defaultNormalStatusText
        slightlyHighStatusText = "It looks like the soil moisture of PLANTNAME has gone over the recommended level.\nPLANTTYPE.name 's soil moisture is at best when around ???~??? UNITs, PLANTNAME 's is currently PLANTSOIL-RECCOMENDEDSOIL higher."
        criticallyHighStatusText = "ATTENTION! PLANTNAME's soil moisture is critically high!\nPLANTTYPE.name 's soil moisture is at best when around ???~??? UNITs, PLANTNAME 's is currently PLANTHUM-RECOMMENDEDHUM higher."
    #EXPLANATIONS
        #Need more knowledge to make a good explanation
        highExplanation = "A balanced soil moisture is essential to enable PLANTNAME to absorb nutrients from the ground. Having too high of a soil moisture [for extended periods of time] is a sign of too much water, which can [suffocate the plant]. It might also be a sign that there is [X] wrong with the plant."
        lowExplanation = "A balanced soil moisture is essential to enable PLANTNAME to absorb nutrients from the ground. Having too low of a soil moisture [for extended periods of time] is a sign of too little water, which [mitigates PLANTNAME's ability to absorb nutrients]. It might also be a sign that there is [X] wrong with the plant."
    #INSTRUCTIONS
        instructions = "placeholder" #TODO

    #TODO: Choose the right strings according to some heurestics
        return(criticallyLowStatusText, lowExplanation, instructions) #arbitrarily chosen for now

def lumAnalysis(luminosity): #These copypasted statusTexts don't really work with luminosity, as luminosity is more dependent on time of the day, previous conditions, etc than the other parameters.
    #STATUSTEXTS
        criticallyLowStatusText = "ATTENTION! PLANTNAME's luminosity is critically low!\nPLANTTYPE.name 's luminosity is at best when around ???~??? lux[per day?], PLANTNAME is currently RECOMMENDEDLUM-PLANTLUM lower."
        slightlyLowStatusText = "It looks like the luminosity of PLANTNAME has gone under the recommended level.\nPLANTTYPE.name 's luminosity is at best when around ???~??? lux[/per day?], PLANTNAME 's is currently RECCOMENDEDLUM-PLANTLUM lower."
        normalStatusText = defaultNormalStatusText
        slightlyHighStatusText = "It looks like the luminosity of PLANTNAME has gone over the recommended level.\nPLANTTYPE.name 's luminosity is at best when around ???~??? lux[/per day?], PLANTNAME 's is currently PLANTLUM-RECCOMENDEDLUM higher."
        criticallyHighStatusText = "ATTENTION! PLANTNAME's luminosity is critically high!\nPLANTTYPE.name 's luminosity is at best when around ???~??? lux[/per day?], PLANTNAME 's is currently PLANTLUM-RECOMMENDEDLUM higher."
    #EXPLANATIONS
        if True:#PLANT.type = "shadow plant":
            highExplanation = "PLANT is a shadow plant, which means it does not need much sunlight. High light levels can damage the leaf, and [stop it from doing evapotranspiration]."
            lowExplanation = "PLANT is a shadow plant, which means it does not need much sunlight. Low light levels can limit the amount of [blue light] that reach PLANTNAME's [photoreceptors], and stop it from doing photosynthesis."
        elif False:#PLANT.type = "light plant": #forgot the actual scientific name
            highExplanation = "PLANT is a light plant, which means it needs a lot of sunlight. Even so, [High light levels can damage the leaf, and [stop it from doing evapotranspiration].]"
            lowExplanation = "PLANT is a light plant, which means it needs a lot of sunlight. Low light levels can limit the amount of [blue light] that reach PLANTNAME's [photoreceptors], and stop it from doing photosynthesis."
    #INSTRUCTIONS
        instructions = "placeholder" #TODO

    #TODO: Choose the right strings according to some heurestics
        return(normalStatusText, "neutral explanation", instructions) #arbitrarily chosen for now

        
"""
    EVERYTHING UNDER THIS POINT IS A BACK UP OF THE TEXT DRAFTS!
"""


"""
    DRAFT STATUSTEXTS:

    defaultNormalStatusText = "Everything seems to be in order."

        VPD: 
        STATUSTEXTS
            optimalVpdStatusText = "PLANTNAME's VPD (vapor pressure deficit) is looking great."
            #With this implementation it's impossible to know X or Y.
            okayVpdStatusText = "PLANTNAME's VPD (vapor pressure deficit)is looking okay, but it could be better. Changing the temperature by X degrees, or changing the humidity by Y % would make it even better!"
            #With this implementation it's impossible to know X or Y.
            badVpdStatusText = "ATTENTION! PLANTNAME's VPD (vapor pressure deficit) is looking critically bad. Try to change the temperature by [at least] X degrees, or change the humidity by [at least] Y % as quickly as possible!"
        EXPLANATIONS
            coldOrDampExplanation = "If the air is cold or damp, less moisture is pulled from the plant, meaning fewer nutrients go into the plant and the plant might develop deficiencies and mould or freeze and die."
            slightlyHotOrDry = "If the air is hot or dry, the difference in vapor pressure can be too great and can cause plants to become stressed under rapid transpiration. This can result in nutrient toxicity due to excessive uptake of nutrients (even if fed with just water).[ One of these nutrient overloads may be calcium, which can lead to chlorosis and stunted growth.]"
            tooHotOrDry = "If the air is too hot or dry, the plant stops growing to save water and closes the cells that release moisture and enable photosynthesis[ (located on the underside of the leaf, called the stomata cells)]."

        TEMP:
        STATUSTEXTS
            criticallyLowStatusText = "ATTENTION! PLANTNAME's temperature is critically low!\nPLANTTYPE.name s are recommended to be kept at ???~???*C, PLANTNAME is currently RECOMMENDEDTEMP-PLANTTEMP lower."
            slightlyLowStatusText = "It looks like the temperature of PLANTNAME has gone under the recommended level.\nPLANTTYPE.name s are recommended to be kept at ???~???*C, PLANTNAME is currently RECCOMENDEDTEMP-PLANTTEMP lower."
            normalStatusText = defaultNormalStatusText
            slightlyHighStatusText = "It looks like the temperature of PLANTNAME has gone over the recommended level.\nPLANTTYPE.name s are recommended to be kept at ???~???*C, PLANTNAME is currently PLANTTEMP-RECCOMENDEDTEMP higher."
            criticallyHighStatusText = "ATTENTION! PLANTNAME's Temperature is critically high!\nPLANTTYPE.name s are recommended to be kept at ???~???*C, PLANTNAME is currently PLANTTEMP-RECOMMENDEDTEMP higher."
        EXPLANATIONS
            #Need more knowledge to make a good explanation  
            highExplanation = "Having a higher temperature makes it harder for PLANTTYPE.name to do photosynthesis. NAR...(something)..."
            lowExplanation = "Having a lower temperature makes it harder for PLANTTYPE.name to do photosynthesis. NAR...(something)..."    

        HUM: #is this useful? is vpd enough?
        STATUSTEXTS
            criticallyLowStatusText = "ATTENTION! PLANTNAME's humidity is critically low!\nPLANTTYPE.name s are recommended to be kept at ???~???% relative humidity, PLANTNAME is currently RECOMMENDEDHUM-PLANTHUM lower."
            slightlyLowStatusText = "It looks like the humidity of PLANTNAME has gone under the recommended level.\nPLANTTYPE.name s are recommended to be kept at ???~???*C, PLANTNAME is currently RECCOMENDEDHUM-PLANTHUM lower."
            normalStatusText = defaultNormalStatusText
            slightlyHighStatusText = "It looks like the humidity of PLANTNAME has gone over the recommended level.\nPLANTTYPE.name s are recommended to be kept at ???~???*C, PLANTNAME is currently PLANTHUM-RECCOMENDEDHUM higher."
            criticallyHighStatusText = "ATTENTION! PLANTNAME's humidity is critically high!\nPLANTTYPE.name s are recommended to be kept at ???~???% relative humidity, PLANTNAME is currently PLANTHUM-RECOMMENDEDHUM higher."
        EXPLANATIONS
            #Need more knowledge to make a good explanation. (also does hum matter for anything else than vpd?)
            highExplanation = "Being in a highly humid environment makes it harder for PLANTTYPE.name to do photosynthesis. ...(something)..."
            lowExplanation = "Being in a highly dry environment makes it harder for PLANTTYPE.name to do photosynthesis. ...(something)..."    
        SOIL:
        STATUSTEXTS
            criticallyLowStatusText = "ATTENTION! PLANTNAME's soil moisture is critically low!\nPLANTTYPE.name 's soil moisture is at best when around ???~??? UNITs, PLANTNAME is currently RECOMMENDEDSOIL-PLANTSOIL lower."
            slightlyLowStatusText = "It looks like the soil moisture of PLANTNAME has gone under the recommended level.\nPLANTTYPE.name 's soil moisture is at best when around ???~??? UNITs, PLANTNAME 's is currently RECCOMENDEDSOIL-PLANTSOIL lower."
            normalStatusText = defaultNormalStatusText
            slightlyHighStatusText = "It looks like the soil moisture of PLANTNAME has gone over the recommended level.\nPLANTTYPE.name 's soil moisture is at best when around ???~??? UNITs, PLANTNAME 's is currently PLANTSOIL-RECCOMENDEDSOIL higher."
            criticallyHighStatusText = "ATTENTION! PLANTNAME's soil moisture is critically high!\nPLANTTYPE.name 's soil moisture is at best when around ???~??? UNITs, PLANTNAME 's is currently PLANTHUM-RECOMMENDEDHUM higher."
        EXPLANATIONS
            #Need more knowledge to make a good explanation
            highExplanation = "A balanced soil moisture is essential to enable PLANTNAME to absorb nutrients from the ground. Having too high of a soil moisture [for extended periods of time] is a sign of too much water, which can ["suffocate the plant"]. It might also be a sign that there is [X] wrong with the plant."
            lowExplanation = "A balanced soil moisture is essential to enable PLANTNAME to absorb nutrients from the ground. Having too low of a soil moisture [for extended periods of time] is a sign of too little water, which [mitigates PLANTNAME's ability to absorb nutrients]. It might also be a sign that there is [X] wrong with the plant."

        LUM: #These copypasted statusTexts don't really work with luminosity, as luminosity is more dependent on time of the day, previous conditions, etc than the other parameters.
        STATUSTEXTS
            criticallyLowStatusText = "ATTENTION! PLANTNAME's luminosity is critically low!\nPLANTTYPE.name 's luminosity is at best when around ???~??? lux[per day?], PLANTNAME is currently RECOMMENDEDLUM-PLANTLUM lower."
            slightlyLowStatusText = "It looks like the luminosity of PLANTNAME has gone under the recommended level.\nPLANTTYPE.name 's luminosity is at best when around ???~??? lux[/per day?], PLANTNAME 's is currently RECCOMENDEDLUM-PLANTLUM lower."
            normalStatusText = defaultNormalStatusText
            slightlyHighStatusText = "It looks like the luminosity of PLANTNAME has gone over the recommended level.\nPLANTTYPE.name 's luminosity is at best when around ???~??? lux[/per day?], PLANTNAME 's is currently PLANTLUM-RECCOMENDEDLUM higher."
            criticallyHighStatusText = "ATTENTION! PLANTNAME's luminosity is critically high!\nPLANTTYPE.name 's luminosity is at best when around ???~??? lux[/per day?], PLANTNAME 's is currently PLANTLUM-RECOMMENDEDLUM higher."
        EXPLANATIONS
            if PLANT.type = "shadow plant":
                highExplanation = "PLANT is a shadow plant, which means it does not need much sunlight. High light levels can damage the leaf, and [stop it from doing evapotranspiration]."
                lowExplanation = "PLANT is a shadow plant, which means it does not need much sunlight. Low light levels can limit the amount of [blue light] that reach PLANTNAME's [photoreceptors], and stop it from doing photosynthesis."
            elif PLANT.type = "light plant": #forgot the actual scientific name
                highExplanation = "PLANT is a light plant, which means it needs a lot of sunlight. Even so, [High light levels can damage the leaf, and [stop it from doing evapotranspiration].]"
                lowExplanation = "PLANT is a light plant, which means it needs a lot of sunlight. Low light levels can limit the amount of [blue light] that reach PLANTNAME's [photoreceptors], and stop it from doing photosynthesis."


"""