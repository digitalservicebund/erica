import datetime

from pydantic import BaseModel


class AuditedModel(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    creator_id: str
