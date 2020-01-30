import requests
import xml.etree.ElementTree as ET

def getPlantData(raspid):
  
    message = ("""<omiEnvelope xmlns="http://www.opengroup.org/xsd/omi/1.0/" version="1.0" ttl="0">
  <read msgformat="odf">
    <msg>
      <Objects xmlns="http://www.opengroup.org/xsd/odf/1.0/">
        <Object>
          <id>""" + raspid + """</id>
        </Object>
      </Objects>
    </msg>
  </read>
</omiEnvelope>
	""")

    req = requests.post("http://greenthumb.cs.aalto.fi:8080", data=message)


    plantlist = []
    
    OML_NS = "{http://www.opengroup.org/xsd/omi/1.0/}"
    ODF_NS = "{http://www.opengroup.org/xsd/odf/1.0/}"

    root = ET.fromstring(req.text)
    response = root.find(f".//{OML_NS}response")
    results = response.findall(f"./{OML_NS}result")

    for result in results:
      objects = result.findall(f"./{OML_NS}msg/{ODF_NS}Objects/{ODF_NS}Object")
      for object in objects:
        inner_object = object.find(f"./{ODF_NS}Object")
        inner_object_id = inner_object.find(f"./{ODF_NS}id").text
        if inner_object_id.startswith("ESP"):
            plantlist.append(inner_object_id)

    return plantlist   


def getData(id):


    message = ("""<omiEnvelope xmlns="http://www.opengroup.org/xsd/omi/1.0/" version="1.0" ttl="0">
  <read msgformat="odf" newest="10">
    <msg>
      <Objects xmlns="http://www.opengroup.org/xsd/odf/1.0/">
        <Object>
          <id>RASP-00000000b6c97266</id>
          <Object>
            <id>""" + str(id) + """</id>
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

    req = requests.post("http://greenthumb.cs.aalto.fi:8080", data=message)

	
    root = ET.fromstring(req.text)
    infoItems = []

    numberOfValues = 0 


    
    #print(root.findall(".//").attrib)

    for infoItem in root.findall(".//"):

        #print(infoItem)
        # Find each infoItem such as Humidity, Temperature..
        if infoItem.attrib.get('name') != None:
            #if infoItem.attrib.get('name') == "deviceID":
              #print(infoItem.findall(".//"))
            
            Dictionary = {}
            Dictionary[infoItem.attrib.get('name')] = []

            #print(infoItem.attrib.get('name'))

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