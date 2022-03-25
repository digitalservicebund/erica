import datetime

from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input import GrundsteuerData
from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_eigentuemer import Vertreter, \
    Empfangsbevollmaechtigter, Person, Eigentuemer
from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_gebaeude import Gebaeude
from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_grundstueck import Grundstueck, Flurstueck


class Builder:
    def __init__(self):
        self.dict = {}

    def build(self):
        return {
            **self.dict
        }


class SampleAdresse(Builder):
    def strasse(self, strasse):
        self.dict["strasse"] = strasse
        return self

    def hausnummer(self, hausnummer):
        self.dict["hausnummer"] = hausnummer
        return self

    def hausnummerzusatz(self, hausnummerzusatz):
        self.dict["hausnummerzusatz"] = hausnummerzusatz
        return self

    def zusatzangaben(self, zusatzangaben):
        self.dict["zusatzangaben"] = zusatzangaben
        return self

    def postfach(self, postfach):
        self.dict["postfach"] = postfach
        return self

    def plz(self, plz):
        self.dict["plz"] = plz
        return self

    def ort(self, ort):
        self.dict["ort"] = ort
        return self

    def bundesland(self, bundesland):
        self.dict["bundesland"] = bundesland
        return self


class SampleName(Builder):
    def anrede(self, anrede):
        self.dict["anrede"] = anrede
        return self

    def titel(self, titel):
        self.dict["titel"] = titel
        return self

    def name(self, name):
        self.dict["name"] = name
        return self

    def vorname(self, vorname):
        self.dict["vorname"] = vorname
        return self

    def geburtsdatum(self, geburtsdatum):
        self.dict["geburtsdatum"] = geburtsdatum
        return self


class SampleFlurstueck(Builder):
    def __init__(self):
        super().__init__()
        self.dict = {
            "angaben": {
                "grundbuchblattnummer": "1A",
                "gemarkung": "random gemarkung",
            },
            "flur": {
                "flur": 1,
                "flurstueck_zaehler": 7,
                "flurstueck_nenner": "7",
            },
            "groesse_qm": 42,
        }

    def gemarkung(self, gemarkung):
        self.dict["angaben"]["gemarkung"] = gemarkung
        return self

    def grundbuchblattnummer(self, grundbuchblattnummer):
        self.dict["angaben"]["grundbuchblattnummer"] = grundbuchblattnummer
        return self

    def groesse(self, groesse):
        self.dict["groesse_qm"] = groesse
        return self

    def flur(self, flur):
        self.dict["flur"]["flur"] = flur
        return self

    def flurstueck_zaehler(self, zaehler):
        self.dict["flur"]["flurstueck_zaehler"] = zaehler
        return self

    def flurstueck_nenner(self, nenner):
        self.dict["flur"]["flurstueck_nenner"] = nenner
        return self

    def w_einheit_zaehler(self, zaehler):
        self.dict["flur"]["wirtschaftliche_einheit_zaehler"] = zaehler
        return self

    def w_einheit_nenner(self, nenner):
        self.dict["flur"]["wirtschaftliche_einheit_nenner"] = nenner
        return self

    def parse(self):
        return Flurstueck.parse_obj(self.build())


class SampleGrundstueck(Builder):
    adresse: SampleAdresse

    def __init__(self):
        super().__init__()
        self.adresse = SampleAdresse().strasse("Madeupstr").hausnummer("22").hausnummerzusatz("b").plz("33333").ort(
            "Bielefeld").bundesland("BE")
        self.dict = {
            "steuernummer": "2181508150",
            "typ": "einfamilienhaus",
            "innerhalb_einer_gemeinde": True,
            "bodenrichtwert": "41,99",
            "flurstueck": [
            ]
        }

    def strasse(self, strasse):
        self.adresse.strasse(strasse)
        return self

    def hausnummer(self, hausnummer):
        self.adresse.hausnummer(hausnummer)
        return self

    def hausnummerzusatz(self, hausnummerzusatz):
        self.adresse.hausnummerzusatz(hausnummerzusatz)
        return self

    def zusatzangaben(self, zusatzangaben):
        self.adresse.zusatzangaben(zusatzangaben)
        return self

    def plz(self, plz):
        self.adresse.plz(plz)
        return self

    def ort(self, ort):
        self.adresse.ort(ort)
        return self

    def bundesland(self, bundesland):
        self.adresse.dict['bundesland'] = bundesland
        return self

    def steuernummer(self, steuernummer):
        self.dict["steuernummer"] = steuernummer
        return self

    def typ(self, typ):
        self.dict["typ"] = typ
        return self

    def innerhalb_einer_gemeinde(self, flag):
        self.dict["innerhalb_einer_gemeinde"] = flag
        return self

    def abweichende_enwticklung(self, zustand):
        self.dict["abweichende_entwicklung"] = zustand
        return self

    def bodenrichtwert(self, bodenrichtwert):
        self.dict["bodenrichtwert"] = bodenrichtwert
        return self

    def flurstuck(self, flurstueck: SampleFlurstueck):
        self.dict["flurstueck"].append(flurstueck)
        return self

    def build(self):
        self.dict["adresse"] = self.adresse.build()
        return super().build()

    def parse(self):
        return Grundstueck.parse_obj(self.build())


class SampleGebaeude(Builder):
    def __init__(self):
        super().__init__()
        self.dict = {
            "ab1949": {
                "is_ab1949": False,
            },
            "kernsaniert": {
                "is_kernsaniert": False,
            },
            "abbruchverpflichtung": {
                "has_abbruchverpflichtung": False,
            },
            "weitere_wohnraeume": {
                "has_weitere_wohnraeume": False,
            },
            "garagen": {
                "has_garagen": False,
            },
        }

    def with_baujahr(self, baujahr=None):
        self.dict["ab1949"]["is_ab1949"] = True
        if baujahr:
            self.dict["baujahr"] = {"baujahr": baujahr}
        return self

    def with_kernsanierung(self, kernsanierungsjahr=None):
        self.dict["kernsaniert"]["is_kernsaniert"] = True
        if kernsanierungsjahr:
            self.dict["kernsanierungsjahr"] = {"kernsanierungsjahr": kernsanierungsjahr}
        return self

    def with_abbruchverpflichtung(self, abbruchverpflichtungsjahr=None):
        self.dict["abbruchverpflichtung"]["has_abbruchverpflichtung"] = True
        if abbruchverpflichtungsjahr:
            self.dict["abbruchverpflichtungsjahr"] = {"abbruchverpflichtungsjahr": abbruchverpflichtungsjahr}
        return self

    def with_wohnflaechen(self, *wohnflaechen: int):
        self.dict["wohnflaechen"] = list(wohnflaechen)
        return self

    def with_weitere_wohnraeume(self, flaeche=0, anzahl=0):
        self.dict["weitere_wohnraeume"]["has_weitere_wohnraeume"] = True
        if anzahl > 0:
            self.dict["weitere_wohnraeume_details"] = {"anzahl": anzahl, "flaeche": flaeche}
        return self

    def with_garagen(self, anzahl_garagen=None):
        self.dict["garagen"]["has_garagen"] = True
        if anzahl_garagen:
            self.dict["garagen_anzahl"] = {"anzahl_garagen": anzahl_garagen}
        return self

    def parse(self):
        return Gebaeude.parse_obj(self.build())


class SampleVertreter(Builder):
    name: SampleName
    adresse: SampleAdresse

    def __init__(self):
        super().__init__()
        self.name = SampleName().anrede("no_anrede").name("Shacklebolt").vorname("Kingsley")
        self.adresse = SampleAdresse().plz("98765").ort("Godric's Hollow")

    def complete(self):
        self.name.titel("Prof.")
        self.dict["telefonnummer"] = {"telefonnummer": "32168"}
        self.adresse.postfach("32263").strasse("Diagon Alley").hausnummer("04").hausnummerzusatz("b")
        return self

    def build(self):
        self.dict["name"] = self.name.build()
        self.dict["adresse"] = self.adresse.build()
        return super().build()

    def parse(self):
        return Vertreter.parse_obj(self.build())


class SampleBevollmaechtigter(Builder):
    name: SampleName
    adressse: SampleAdresse

    def __init__(self):
        super().__init__()
        self.name = SampleName().anrede("frau").name("McGonagall").vorname("Minerva")
        self.adressse = SampleAdresse().plz("08642").ort("Hogsmeade")

    def with_title(self):
        self.name.titel("Prof.")
        return self

    def with_strasse(self):
        self.adressse.strasse("Diagon Alley").hausnummer(3).hausnummerzusatz("c")
        return self

    def with_postfach(self):
        self.adressse.postfach("34567")
        return self

    def with_telefonnummer(self):
        self.dict["telefonnummer"] = {"telefonnummer": "123-456"}
        return self

    def complete(self):
        return self.with_title().with_strasse().with_postfach().with_telefonnummer()

    def build(self):
        self.dict["name"] = self.name.build()
        self.dict["adresse"] = self.adressse.build()
        return super().build()

    def parse(self):
        return Empfangsbevollmaechtigter.parse_obj(self.build())


class SamplePerson(Builder):
    name: SampleName
    adresse: SampleAdresse

    def __init__(self):
        super().__init__()
        self.name = SampleName().anrede("frau").name("Granger").vorname("Hermione")
        self.adresse = SampleAdresse().plz("7777").ort("London")
        self.dict = {
            "steuer_id": {
                "steuer_id": "04452317681",
            },
            "anteil": {
                "zaehler": 1,
                "nenner": 1,
            },
        }

    def vorname(self, vorname):
        self.name.vorname(vorname)
        return self

    def with_telefonnummer(self):
        self.dict["telefonnummer"] = {"telefonnummer": "123"}
        return self

    def with_vertreter(self):
        self.dict["vertreter"] = SampleVertreter().build()
        return self

    def complete(self):
        self.with_telefonnummer()
        self.name.titel("Prof").geburtsdatum(datetime.date(1979, 9, 19))

    def build(self):
        self.dict["persoenlicheAngaben"] = self.name.build()
        self.dict["adresse"] = self.adresse.build()
        return super().build()

    def parse(self):
        return Person.parse_obj(self.build())


class SampleEigentuemer(Builder):
    def __init__(self):
        super().__init__()
        self.dict = {
            "person": [],
        }

    def person(self, person):
        self.dict["person"].append(person)
        return self

    def verheiratet(self, are_verheiretet: bool):
        self.dict["verheiratet"] = {"are_verheiratet": are_verheiretet}
        return self

    def empfangsbevollmaechtigter(self, empfangsbevollmaechtigter):
        self.dict["empfangsbevollmaechtigter"] = empfangsbevollmaechtigter
        return self

    def parse(self):
        return Eigentuemer.parse_obj(self.dict)


class DefaultSampleEigentuemer(SampleEigentuemer):
    def __init__(self):
        super().__init__()
        self.person(SamplePerson().build())


class SampleGrundsteuerData(Builder):
    grundstueck: SampleGrundstueck
    gebaeude: Optional[SampleGebaeude]
    eigentuemer: SampleEigentuemer

    def __init__(self):
        super().__init__()
        self.grundstueck = SampleGrundstueck()
        self.gebaeude = SampleGebaeude().with_wohnflaechen(42)
        self.eigentuemer = DefaultSampleEigentuemer()

        self.dict = {
            "freitext": ""
        }

    def with_empfangsvollmacht(self):
        self.eigentuemer.empfangsbevollmaechtigter(SampleBevollmaechtigter().build())
        return self

    def with_grundstueck(self, grundstueck: SampleGrundstueck):
        self.grundstueck = grundstueck
        return self

    def without_gebaeude(self):
        self.gebaeude = None
        return self

    def build(self):
        self.dict["grundstueck"] = self.grundstueck.build()
        self.dict["gebaeude"] = self.gebaeude.build()
        self.dict["eigentuemer"] = self.eigentuemer.build()
        return super().build()

    def parse(self):
        return GrundsteuerData.parse_obj(self.build())
