from datetime import datetime
from pydantic import BaseModel


class AuditedModel(BaseModel):
    created_at: datetime
    updated_at: datetime
    creator_id: str
