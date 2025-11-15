from pydantic import BaseModel
from datetime import datetime

class URLBase(BaseModel):
    target_url: str

class URLCreate(URLBase):
    slug: str

class URLResponse(URLBase):
    id: int
    slug: str
    created_at: datetime
    hits: int

    class Config:
        orm_mode = True
