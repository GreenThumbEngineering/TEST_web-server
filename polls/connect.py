import requests
import xml.etree.ElementTree as ET

def getData():


    message = ("""<omiEnvelope xmlns="http://www.opengroup.org/xsd/omi/1.0/" version="1.0" ttl="0">
  <read msgformat="odf" newest="10">
    <msg>
      <Objects xmlns="http://www.opengroup.org/xsd/odf/1.0/">
        <Object>
          <id>RASP-00000000b6c97266</id>
          <Object>
            <id>ESP32-18DB4512CFA4</id>
            <InfoItem name="ColorTemp"/>
            <InfoItem name="Humidity"/>
            <InfoItem name="Lux"/>
            <InfoItem name="RGB"/>
            <InfoItem name="Pressure"/>
            <InfoItem name="Temperature"/>
            <InfoItem name="Soil"/>
            <InfoItem name="Time"/>
            <InfoItem name="deviceID"/>
          </Object>
        </Object>
      </Objects>
    </msg>
  </read>
</omiEnvelope>
	""")

    req = requests.post("http://82.130.44.157:8080/", data=message)

	
    root = ET.fromstring(req.text)
    infoItems = []

    numberOfValues = 0 

    for infoItem in root.findall(".//"):

        # Find each infoItem such as Humidity, Temperature..
        if infoItem.attrib.get('name') != None:
            Dictionary = {}
            Dictionary[infoItem.attrib.get('name')] = []

            values = infoItem
            # This is only to get the number of values in total
            numberOfValues = 0
            # All values under one infoItem such as Humidity
            for value in values.findall(".//"):
                Dictionary[infoItem.attrib.get('name')].append(value.text)
                numberOfValues += 1 

            infoItems.append(Dictionary)

    # Take each row separately
    eachRowAsDictionary = []
    i = 0
   
    while i < numberOfValues -1 :
        Dict = {}

        for stamp in infoItems:

            for key in stamp.keys(): 

                for value in stamp.values():
                    Dict[key] = value[i]
        
        eachRowAsDictionary.append(dict(Dict))
        
        i+=1

    return eachRowAsDictionary