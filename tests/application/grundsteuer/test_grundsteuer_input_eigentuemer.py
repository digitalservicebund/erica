import pytest
from pydantic import ValidationError

from erica.application.grundsteuer.grundsteuer_input_eigentuemer import Person, PersoenlicheAngaben, Anteil, Adresse, \
    Eigentuemer


class TestEigentuemer:
    @pytest.mark.parametrize("persons",
                             [([Person(persoenliche_angaben=PersoenlicheAngaben(anrede="frau", name="daViella",
                                                                                vorname="Gruella"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="04452317681", anteil=Anteil(zaehler="1", nenner="2"))]),
                              ([Person(persoenliche_angaben=PersoenlicheAngaben(anrede="frau", name="daViella",
                                                                                vorname="Gruella"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="04452317681", anteil=Anteil(zaehler="1", nenner="2")),
                                Person(persoenliche_angaben=PersoenlicheAngaben(anrede="herr", name="Man",
                                                                                vorname="Robin"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="09952417688", anteil=Anteil(zaehler="1", nenner="2")),
                                Person(persoenliche_angaben=PersoenlicheAngaben(anrede="frau", name="Biest",
                                                                                vorname="Bella"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="03352417692", anteil=Anteil(zaehler="1", nenner="2"))])],
                             ids=["single", "three_people"])
    def test_if_no_couple_and_verheiratet_not_set_then_raise_no_error(self, persons):
        try:
            Eigentuemer.parse_obj({"person": persons})
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    @pytest.mark.parametrize("persons",
                             [([Person(persoenliche_angaben=PersoenlicheAngaben(anrede="frau", name="daViella",
                                                                                vorname="Gruella"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="04452317681", anteil=Anteil(zaehler="1", nenner="2"))]),
                              ([Person(persoenliche_angaben=PersoenlicheAngaben(anrede="frau", name="daViella",
                                                                                vorname="Gruella"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="04452317681", anteil=Anteil(zaehler="1", nenner="2")),
                                Person(persoenliche_angaben=PersoenlicheAngaben(anrede="herr", name="Man",
                                                                                vorname="Robin"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="09952417688", anteil=Anteil(zaehler="1", nenner="2")),
                                Person(persoenliche_angaben=PersoenlicheAngaben(anrede="frau", name="Biest",
                                                                                vorname="Bella"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="03352417692", anteil=Anteil(zaehler="1", nenner="2"))])],
                             ids=["single", "three_people"])
    def test_if_no_couple_and_verheiratet_set_then_raise_error(self, persons):
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj({"person": persons, "verheiratet": False})

    @pytest.mark.parametrize("verheiratet", [True, False], ids=["married", "not_married"])
    def test_if_two_persons_set_and_verheiratet_set_then_raise_no_error(self, verheiratet):
        persons = [Person(persoenliche_angaben=PersoenlicheAngaben(anrede="frau", name="daViella",
                                                                                vorname="Gruella"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="04452317681", anteil=Anteil(zaehler="1", nenner="2")),
                                Person(persoenliche_angaben=PersoenlicheAngaben(anrede="frau", name="Biest",
                                                                                vorname="Bella"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="03352417692", anteil=Anteil(zaehler="1", nenner="2"))]
        try:
            Eigentuemer.parse_obj({"person": persons, "verheiratet": verheiratet})
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_two_persons_set_and_verheiratet_not_set_then_raise_error(self):
        persons = [Person(persoenliche_angaben=PersoenlicheAngaben(anrede="frau", name="daViella",
                                                                                vorname="Gruella"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="04452317681", anteil=Anteil(zaehler="1", nenner="2")),
                                Person(persoenliche_angaben=PersoenlicheAngaben(anrede="frau", name="Biest",
                                                                                vorname="Bella"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="03352417692", anteil=Anteil(zaehler="1", nenner="2"))]
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj({"person": persons})

    def test_if_all_persons_have_test_tax_id_number_then_raise_no_error(self):
        persons = [Person(persoenliche_angaben=PersoenlicheAngaben(anrede="frau", name="daViella",
                                                                                vorname="Gruella"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="04452317681", anteil=Anteil(zaehler="1", nenner="2")),
                                Person(persoenliche_angaben=PersoenlicheAngaben(anrede="herr", name="Man",
                                                                                vorname="Robin"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="09952417688", anteil=Anteil(zaehler="1", nenner="2")),
                                Person(persoenliche_angaben=PersoenlicheAngaben(anrede="frau", name="Biest",
                                                                                vorname="Bella"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="03352417692", anteil=Anteil(zaehler="1", nenner="2"))]
        try:
            Eigentuemer.parse_obj({"person": persons})
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_all_persons_have_real_tax_id_number_then_raise_no_error(self):
        persons = [Person(persoenliche_angaben=PersoenlicheAngaben(anrede="frau", name="daViella",
                                                                                vorname="Gruella"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="10796522382", anteil=Anteil(zaehler="1", nenner="2")),
                                Person(persoenliche_angaben=PersoenlicheAngaben(anrede="herr", name="Man",
                                                                                vorname="Robin"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="38689804274", anteil=Anteil(zaehler="1", nenner="2")),
                                Person(persoenliche_angaben=PersoenlicheAngaben(anrede="frau", name="Biest",
                                                                                vorname="Bella"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="43865766025", anteil=Anteil(zaehler="1", nenner="2"))]
        try:
            Eigentuemer.parse_obj({"person": persons})
        except ValidationError as e:
            pytest.fail("parse_obj failed with unexpected ValidationError " + str(e))

    def test_if_persons_have_real_and_test_tax_id_number_then_raise_error(self):
        persons = [Person(persoenliche_angaben=PersoenlicheAngaben(anrede="frau", name="daViella",
                                                                                vorname="Gruella"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="10796522382", anteil=Anteil(zaehler="1", nenner="2")),
                                Person(persoenliche_angaben=PersoenlicheAngaben(anrede="herr", name="Man",
                                                                                vorname="Robin"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="09952417688", anteil=Anteil(zaehler="1", nenner="2")),
                                Person(persoenliche_angaben=PersoenlicheAngaben(anrede="frau", name="Biest",
                                                                                vorname="Bella"),
                                       adresse=Adresse(plz="79618", ort="Rheinfelden"),
                                       steuer_id="03352417692", anteil=Anteil(zaehler="1", nenner="2"))]
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj({"person": persons})
