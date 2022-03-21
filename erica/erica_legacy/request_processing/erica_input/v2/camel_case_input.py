from humps import camelize
from pydantic import BaseModel, validator


class CamelCaseInput(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True

    @validator('*', pre=True)
    def convert_empty_str_to_none(cls, v):
        if v == "":
            return None
        return v
