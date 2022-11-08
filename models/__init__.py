from time import time

from typing import Optional
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