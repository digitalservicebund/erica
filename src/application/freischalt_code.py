from uuid import UUID

from pydantic import BaseModel

from src.domain.freischalt_code import FreischaltCodePayload
from src.domain.status import Status


class FreischaltCodeCreateDto(BaseModel):
    payload: FreischaltCodePayload
    user_id: UUID

    class Config:
        orm_mode = True


class FreischaltCodeDto(BaseModel):
    id: UUID
    status: Status
    payload: FreischaltCodePayload
    user_id: UUID

    class Config:
        orm_mode = True
