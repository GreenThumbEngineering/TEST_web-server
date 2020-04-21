from polls.models import PlantData
import xml.etree.ElementTree as ET
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
####
class ReadWrapper:
    def main(message_read):
        def find_how_many(msg):
            number_of_values = 1
            for i in msg.findall('.//'):
                if i.get('newest') != None:
                    number_of_values = i.get('newest')
                    break
            return number_of_values

        def parse_read(msg,URL):
            dic = {}
            root = msg[0][0][0][0]
            RASP_ID = root.findall('{http://www.opengroup.org/xsd/odf/1.0/}id')[0].text
            for c in root.findall(f"""{URL}Object"""):
                ESP_id = c.findall(f"""{URL}id""")[0].text
                dic[ESP_id] = {}
                attribute_list = []
                for n in c.findall(f"""{URL}InfoItem"""):
                    attribute_list.append(n.attrib["name"])
                dic[ESP_id] = attribute_list
            return dic,RASP_ID

        def read_database(data,PlantData,number_of_values):
            dic = {}
            for key in data.keys():
                dic[key] = list(PlantData.objects.values(*data[key]).filter(DeviceId=key).order_by('-ServerTime'))[:number_of_values]
            return dic

        def create_return_dictionary(arvot,jsoni):
            dic = {}
            for variable in arvot:
                variable_list = []
                dic[variable] = variable_list 
                for values in jsoni:
                    variable_list.append(values[variable])
            return dic


        def create_template(dic):
            create_temp = ""
            create_temp += f"<Object><id>{dic['DeviceId'][0]}</id>"
            for key in dic.keys():
                x=-1
                create_temp +=(f"""<InfoItem name="{key}">""")
                for value in dic[key]:
                    x+=1
                    unixTime = (dic['ServerTime'][x]).timestamp()
                    create_temp += (f"""<value unixTime="{unixTime}" dateTime="{dic['ServerTime'][x]}">{value}</value>""")
                create_temp += "</InfoItem>"
            create_temp += "</Object>"
            return create_temp

        def create_final_read_template(esp_templates,RASP_ID):
            template = f"<Object><id>{RASP_ID}</id>"
            template += esp_templates
            base = (f"""<?xml version='1.0' encoding='UTF-8'?><omiEnvelope xmlns="http://www.opengroup.org/xsd/omi/1.0/" ttl="10.0" version="1.0"><response><result msgformat="odf"><return returnCode="200"/><msg><Objects xmlns="http://www.opengroup.org/xsd/odf/1.0/" version="1.0">{template}</Object></Objects></msg></result></response></omiEnvelope>""")
            return base 

        msg_read = ET.fromstring(message_read)
        URL = '{http://www.opengroup.org/xsd/odf/1.0/}'
        number_of_values = find_how_many(msg_read)
        ESP_DICTIONARY,RASP_ID= parse_read(msg_read,URL)
        data = read_database(ESP_DICTIONARY,PlantData,int(number_of_values))
        esp_template = ""
        for esp in data.keys():
            return_data = create_return_dictionary(ESP_DICTIONARY[esp],data[esp])
            esp_template += create_template(return_data)

        final_template = (parseString(create_final_read_template(esp_template,RASP_ID))).toprettyxml()
        return(final_template)





