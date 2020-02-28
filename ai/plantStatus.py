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

    if soilMoisture >= 2600: # when is too much water?
        return -1
    elif 2200 <= soilMoisture < 2600:
        return 0
    elif 1400 <= soilMoisture < 2200:
        return 1
    else:
        return 2