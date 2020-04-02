import xml.etree.ElementTree as ET
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from polls.models import PlantData

class WriteParser:

    def main(write_message):

        def parse_write(msg,URL):
            dic = {}
            root = msg[0][0][0][0]
            RASP_ID = root.findall('{http://www.opengroup.org/xsd/odf/1.0/}id')[0].text
            for c in root.findall(f"""{URL}Object"""):
                ESP_id = c.findall(f"""{URL}id""")[0].text
                dic[ESP_id] = {}
                attribute_list = {}
                for n in c.findall(f"""{URL}InfoItem"""):
                    for p in n.findall(f"""{URL}value"""):
                        attribute_list[n.attrib['name']] = p.text
                dic[ESP_id] = attribute_list
            return dic,RASP_ID
        def create_templates(rasp_id,ESP_DICTIONARY):
            templates=f"<Object><id>{rasp_id}</id>"
            value_list = ['DeviceId','SystemId','MeasurementTime','Temperature','Humidity','SoilMoisture','Luminosity']
            for esp in ESP_DICTIONARY.keys():
                x=0
                templates += f"<Object><id>{esp}</id>"
                for value in ESP_DICTIONARY[esp]:
                    value2 = ESP_DICTIONARY[esp][value_list[x]]
                    templates += f"""<InfoItem name="{value_list[x]}">
                    <value unixTime="1541609326"
                        dateTime="2018-11-07T18:48:46.359+02:00"
                        >{value2}</value>
                    </InfoItem>"""
                    x+=1
                templates+="</Object>"
            
            templates += "</Object>"
            return templates

        def create_final_message(templates):
            base = f"""
            <omiEnvelope ttl="10" version="1.0" xmlns="http://www.opengroup.org/xsd/omi/1.0/">
            <response>
                <result msgformat="odf">
                <return returnCode="200">
                </return>
                <msg>
                    <Objects xmlns="http://www.opengroup.org/xsd/odf/1.0/">
                    {templates}
                    </Objects>
                </msg>
                </result>
            </response>
            </omiEnvelope>"""
            return base
            
        URL = '{http://www.opengroup.org/xsd/odf/1.0/}'

        msg_write = ET.fromstring(write_message)
        ESP_DICTIONARY,RASP_ID = parse_write(msg_write,URL)
        return ESP_DICTIONARY, RASP_ID
        
        #for esp in ESP_DICTIONARY.keys():
        #    plantData = PlantData.objects.create(
        #    DeviceId = ESP_DICTIONARY[esp]['DeviceId'], SystemId = ESP_DICTIONARY[esp]['SystemId']
        #    , MeasurementTime = ESP_DICTIONARY[esp]['MeasurementTime'],   Temperature = float(ESP_DICTIONARY[esp]['Temperature'])
        #    , Humidity = float(ESP_DICTIONARY[esp]['Humidity'])
        #    , SoilMoisture = int(ESP_DICTIONARY[esp]['SoilMoisture']), Luminosity = int(ESP_DICTIONARY[esp]['Luminosity']))


        #templates = create_templates(RASP_ID,ESP_DICTIONARY)
        #final_template = (parseString(create_final_message(templates))).toprettyxml()
        #return final_template 
