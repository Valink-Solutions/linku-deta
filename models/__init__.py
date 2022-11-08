from time import time

from typing import List, Optional
from pydantic import BaseModel, Field

# Utility Models
class Token(BaseModel):
    access_token: str
    token_type: Optional[str] = 'Bearer'
    
    
class TokenData(BaseModel):
    email: str
    # scopes: dict | None = None
    
    
class Snapshot(BaseModel):
    short_code: str
    clicks: int = 0
    date: float = Field(default_factory=time)
    

class SnapshotResponse(BaseModel):
    count: int
    last: Optional[str] = None
    items: List[Snapshot]

    class Config:
        orm_mode = True