import requests
import xml.etree.ElementTree as ET

def getData():
	r = requests.post("http://82.130.44.157:8080", data=
	"""<omiEnvelope xmlns="http://www.opengroup.org/xsd/omi/1.0/" version="1.0" ttl="0">
	  <read msgformat="odf">
		<msg>
		  <Objects xmlns="http://www.opengroup.org/xsd/odf/1.0/">
			<Object>
			  <id>RASP-00000000b6c97266</id>
			  <Object>
				<id>ESP32-18DB4512CFA4</id>
			  </Object>
			</Object>
		  </Objects>
		</msg>
	  </read>
	</omiEnvelope>
	""")

	Dict = {

	}

	xml = ET.fromstring(r.text)

	for child in xml:
		for n in child:
			for y in n:
				if "msg" in y.tag:
					for o in y:
						for b in o:
							for f in b:
								if ("id" in f.tag):
									Dict["systemID"] = f.text
								else:
									for k in f:

										if ("id" in f.tag):
											Dict["ESPID"] = f.text
										else:
											for l in k:
												Dict[str(k.get('name'))] = str(l.text)
	return Dict