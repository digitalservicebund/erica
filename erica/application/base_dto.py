from humps import camelize
from pydantic import BaseModel, validator


class CamelCaseModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True
        anystr_strip_whitespace = True

    @validator('*', pre=True)
    def convert_empty_str_to_none_before(cls, v):
        return cls.__convert_empty_str_to_none(v)

    @validator('*')
    def convert_empty_str_to_none_after(cls, v):
        return cls.__convert_empty_str_to_none(v)

    @staticmethod
    def __convert_empty_str_to_none(v):
        if v == "":
            return None
        return v


class BaseDto(CamelCaseModel):
    pass
