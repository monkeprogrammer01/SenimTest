from pydantic import Field
from datetime import datetime
from pydantic import BaseModel


class ReportCreate(BaseModel):
    category: str = Field(...)
    message: str = Field(..., min_length=1)


class ReportOut(BaseModel):
    id: int
    category: str
    message: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True