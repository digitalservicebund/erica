from dataclasses import asdict
from pprint import pprint

import xmlschema

from erica.elster_xml.grundsteuer.elster_data_representation import EGrundsteuerData

basic_xml_beginning = """<?xml version="1.0" encoding="UTF-8"?>
<Elster xmlns="http://www.elster.de/elsterxml/schema/v11">
	<TransferHeader version="11">
		<Verfahren>ElsterErklaerung</Verfahren>
		<DatenArt>Grundsteuerwert</DatenArt>
		<Vorgang>send-Auth</Vorgang>
		<Testmerker>700000004</Testmerker>
		<HerstellerID>74931</HerstellerID>
		<DatenLieferant>ERiC Entwicklung</DatenLieferant>
		<Datei>
			<Verschluesselung>CMSEncryptedData</Verschluesselung>
			<Kompression>GZIP</Kompression>
			<TransportSchluessel/>
		</Datei>
	</TransferHeader>
	<DatenTeil>
		<Nutzdatenblock>
			<NutzdatenHeader version="11">
				<NutzdatenTicket>adfjasldkfuweor456asvs</NutzdatenTicket>
				<Empfaenger id="F">1121</Empfaenger>
				<Hersteller>
					<ProduktName>ERICTest</ProduktName>
					<ProduktVersion>2009.1/0</ProduktVersion>
				</Hersteller>
				<DatenLieferant>Softwaretester ERiC</DatenLieferant>
			</NutzdatenHeader>
			<Nutzdaten>
"""

basic_xml_ending = """
</Nutzdaten>
		</Nutzdatenblock>
	</DatenTeil>
</Elster>"""


def convert_to_grundsteuer_xml(grundsteuer_object: EGrundsteuerData):
    dict_data_representation = asdict(grundsteuer_object)
    dict_data_representation["@version"] = '2'
    dict_data_representation["@xmlns"] = 'http://finkonsens.de/elster/elstererklaerung/grundsteuerwert/e88/v2'
    pprint(dict_data_representation)
    grundsteuer_schema = xmlschema.XMLSchema('./erica/elster_xml/grundsteuer/Grundsteuerwert-2.xsd')
    grundsteuer_schema_encoded = grundsteuer_schema.encode(dict_data_representation, validation='lax')
    print("SCHEMA ERRORS: " + str(grundsteuer_schema_encoded[1]))
    return basic_xml_beginning + xmlschema.etree_tostring(grundsteuer_schema_encoded[0],
                                                          {
                                                              "": "http://finkonsens.de/elster/elstererklaerung/grundsteuerwert/e88/v2"}) + basic_xml_ending
