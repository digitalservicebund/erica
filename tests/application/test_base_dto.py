from erica.application.base_dto import CamelCaseModel


class CamelCaseModelChild(CamelCaseModel):
    name_of_pet: str
    person_a_name: str


class TestCamelCaseModel:

    def test_if_parsed_from_dict_with_snake_case_attribute_then_transform_to_object_with_snake_case_attributes(self):
        name_of_pet = 'Pickett'
        person_a_name = 'Newt'
        resulting_object = CamelCaseModelChild.parse_obj({'name_of_pet': name_of_pet, 'person_a_name': person_a_name})

        assert resulting_object.name_of_pet == name_of_pet
        assert resulting_object.person_a_name == person_a_name

    def test_if_parsed_from_dict_with_camel_case_attribute_then_transform_to_object_with_snake_case_attributes(self):
        name_of_pet = 'Pickett'
        person_a_name = 'Newt'
        resulting_object = CamelCaseModelChild.parse_obj({'nameOfPet': name_of_pet, 'person_a_name': person_a_name})

        assert resulting_object.name_of_pet == name_of_pet

    def test_if_converted_to_dict_by_alias_then_generate_camel_case_attributes(self):
        name_of_pet = 'Pickett'
        person_a_name = 'Newt'
        obj = CamelCaseModelChild.parse_obj({'nameOfPet': name_of_pet, 'person_a_name': person_a_name})

        resulting_dict = obj.dict(by_alias=True)

        assert resulting_dict['nameOfPet'] == name_of_pet
        assert resulting_dict['personAName'] == person_a_name
